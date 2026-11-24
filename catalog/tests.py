from django.test import TestCase


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

class ItemAdminTestCase(TestCase):
    """The Item admin mixes in django-clone, which overrides private admin API."""

    fixtures = ['catalog_test_data.yaml']

    def setUp(self):
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_superuser('admin', password='pw')
        self.client.force_login(user)

    def get(self, path):
        return self.client.get(path, HTTP_HOST='admin.localhost')

    def test_changelist_offers_duplicate_action(self):
        resp = self.get('/catalog/item/')
        self.assertEqual(resp.status_code, 200)
        actions = [name for name, _ in resp.context['action_form'].fields['action'].choices]
        self.assertIn('make_clone', actions)
        self.assertIn('delete_selected', actions)

    def test_add_form_renders(self):
        self.assertEqual(self.get('/catalog/item/add/').status_code, 200)

    def test_change_form_shows_duplicate_link(self):
        resp = self.get('/catalog/item/1/change/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '?duplicate=true')

    def test_duplicate_link_clones_item(self):
        from catalog.models import Item

        before = Item.objects.count()
        resp = self.get('/catalog/item/1/change/?duplicate=true')
        self.assertEqual(Item.objects.count(), before + 1)
        clone = Item.objects.latest('pk')
        self.assertRedirects(
            resp, f'/catalog/item/{clone.pk}/change/', fetch_redirect_response=False
        )

    def test_duplicate_action_clones_items(self):
        from catalog.models import Item

        before = Item.objects.count()
        resp = self.client.post(
            '/catalog/item/',
            {'action': 'make_clone', '_selected_action': ['1']},
            HTTP_HOST='admin.localhost',
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Item.objects.count(), before + 1)
