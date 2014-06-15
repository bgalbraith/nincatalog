from django.test import TestCase


class CatalogViewsTestCase(TestCase):
    fixtures = ['catalog_testdata.yaml']

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_category(self):
        resp = self.client.get('/strobe-light/')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get('/the-fragile/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('category' in resp.context)

        category = resp.context['category']
        self.assertEqual(category.pk, 14)
        self.assertEqual(category.name, 'The Fragile')