from django.test import TestCase

from catalog.models import Item, MusicLabel


class CatalogViewsTestCase(TestCase):
    fixtures = ['catalog_test_data.yaml']

    def test_index_view(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_category_view_invalid_category(self):
        resp = self.client.get('/strobe-light/')
        self.assertEqual(resp.status_code, 404)

    def test_category_view_valid_category(self):
        resp = self.client.get('/the-fragile/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('listing' in resp.context)

        listing = resp.context['listing']
        self.assertEqual(len(listing['categories']), 1)

        category = listing['categories'][0]
        self.assertEqual(category['name'], 'The Fragile')

    def test_category_view_item_list(self):
        resp = self.client.get('/the-fragile/')
        listing = resp.context['listing']
        category = listing['categories'][0]
        self.assertEqual(category['items'].count(), 1)

        item = category['items'].first()
        self.assertEqual(item.pk, 1)
        self.assertEqual(item.name, "The Fragile")

    def test_item_view_invalid_category_invalid_item(self):
        resp = self.client.get('/strobe-light/2/')
        self.assertEqual(resp.status_code, 404)

    def test_item_view_valid_category_invalid_item(self):
        resp = self.client.get('/the-fragile/2/')
        self.assertEqual(resp.status_code, 404)

    def test_item_view_invalid_category_valid_item(self):
        resp = self.client.get('/strobe-light/1/')
        self.assertEqual(resp.status_code, 404)

    def test_item_view_valid_category_valid_item(self):
        resp = self.client.get('/the-fragile/1/')
        self.assertTrue(resp.status_code, 200)
        self.assertTrue('item' in resp.context)

        item = resp.context['item']
        self.assertEqual(item.pk, 1)
        self.assertEqual(item.name, "The Fragile")

class ItemTagTestCase(TestCase):
    """Issue #96: an underscore in an item's name broke its links."""

    fixtures = ['catalog_test_data.yaml']

    def setUp(self):
        self.item = Item.objects.get(pk=1)
        self.item.name = 'tourbook: with_teeth 2006'
        self.item.old_key = '01-90026'
        self.item.save()

    def test_tag_has_no_underscores(self):
        self.assertNotIn('_', self.item.tag())

    def test_listing_links_to_item(self):
        resp = self.client.get('/the-fragile/')
        self.assertContains(resp, f'href="/the-fragile/{self.item.tag()}/"')
        self.assertNotContains(resp, 'href=""')

    def test_item_page_loads_from_tag(self):
        resp = self.client.get(f'/the-fragile/{self.item.tag()}/')
        self.assertEqual(resp.status_code, 200)

    def test_legacy_url_redirects_to_item(self):
        resp = self.client.get('/item.asp', {'key': '01-90026'})
        self.assertRedirects(
            resp, f'/the-fragile/{self.item.tag()}/',
            status_code=301, fetch_redirect_response=False,
        )


class ItemAdminTestCase(TestCase):
    fixtures = ['catalog_test_data.yaml']

    def setUp(self):
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_superuser('admin', password='pw')
        self.client.force_login(user)
        self.item = Item.objects.get(pk=1)
        self.item.old_key = 'LEGACY01'
        self.item.save()
        extra_label = MusicLabel.objects.create(name='Interscope')
        self.item.music_labels.set([MusicLabel.objects.first(), extra_label])

    def get(self, path):
        return self.client.get(path, HTTP_HOST='admin.localhost')

    def post(self, path, data):
        return self.client.post(path, data, HTTP_HOST='admin.localhost')

    def assertIsCopyOfItem(self, copy):
        self.assertNotEqual(copy.pk, self.item.pk)
        self.assertEqual(copy.name, self.item.name)
        self.assertEqual(copy.category, self.item.category)
        self.assertIsNone(copy.old_key)
        self.assertQuerySetEqual(
            copy.music_labels.order_by('pk'),
            self.item.music_labels.order_by('pk'),
        )

    def test_changelist_offers_duplicate_action(self):
        resp = self.get('/catalog/item/')
        self.assertEqual(resp.status_code, 200)
        actions = [name for name, _ in resp.context['action_form'].fields['action'].choices]
        self.assertIn('duplicate', actions)
        self.assertIn('delete_selected', actions)

    def test_add_form_renders(self):
        self.assertEqual(self.get('/catalog/item/add/').status_code, 200)

    def test_change_form_offers_duplicate_action(self):
        resp = self.get('/catalog/item/1/change/')
        self.assertEqual(resp.status_code, 200)
        actions = [name for name, _ in resp.context['action_form'].fields['action'].choices]
        self.assertEqual(actions[1:], ['duplicate'])

    def test_duplicate_from_change_form_opens_copy(self):
        resp = self.post(
            '/catalog/item/1/change/',
            {'CHANGE_FORM-action': 'duplicate', '_selected_action': ['1']},
        )
        copy = Item.objects.latest('pk')
        self.assertIsCopyOfItem(copy)
        self.assertRedirects(
            resp, f'/catalog/item/{copy.pk}/change/', fetch_redirect_response=False
        )

    def test_duplicate_from_changelist_copies_each_selected(self):
        other = Item.objects.get(pk=1)
        other.pk = None
        other.name = 'Other Item'
        other.save()
        before = Item.objects.count()
        resp = self.post(
            '/catalog/item/',
            {'action': 'duplicate', '_selected_action': ['1', str(other.pk)]},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Item.objects.count(), before + 2)
        self.assertIsCopyOfItem(Item.objects.filter(name=self.item.name).latest('pk'))
