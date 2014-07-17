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