from django.conf import settings
from django.contrib.staticfiles import finders
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from pathlib import Path
import io
import re

from merch.models import Poster


class PosterTestCase(TestCase):
    def setUp(self):
        # Create a test image
        self.test_image = self.create_test_image()
        
        # Create a test poster
        self.poster = Poster.objects.create(
            submitter_name="Test User",
            image=self.test_image
        )

    def create_test_image(self):
        """Create a simple test image"""
        # Create a simple image using PIL
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )

    def test_poster_creation(self):
        """Test that posters can be created"""
        self.assertEqual(self.poster.submitter_name, "Test User")
        self.assertTrue(self.poster.image)

    def test_posters_view(self):
        """Test the posters view loads"""
        client = Client(HTTP_HOST='merch.localhost')
        response = client.get('/peelitback2025poster/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")

    def test_poster_gallery_view_requires_ajax(self):
        """A plain GET is a 404 by design.

        The gallery is AJAX-only: static/merch/js/posters.js sends
        X-Requested-With explicitly, and no poster_gallery template exists,
        so the non-AJAX branch of the view raises Http404.
        """
        client = Client(HTTP_HOST='merch.localhost')
        response = client.get(f'/poster-gallery/{self.poster.id}/')
        self.assertEqual(response.status_code, 404)

    def test_poster_gallery_ajax_view(self):
        """Test the poster gallery AJAX endpoint returns all posters"""
        client = Client(HTTP_HOST='merch.localhost')
        response = client.get(
            f'/poster-gallery/{self.poster.id}/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = response.json()
        self.assertIn('posters', data)
        self.assertIn('initial_index', data)
        self.assertEqual(len(data['posters']), 1)  # Only our test poster exists
        self.assertEqual(data['initial_index'], 0)
        self.assertEqual(data['posters'][0]['submitter_name'], 'Test User')

    def test_multiple_posters_gallery(self):
        """Every poster is returned, with initial_index on the clicked one.

        Order is per-session random (get_random_posters_for_session), so the
        index is deliberately not asserted against insertion order.
        """
        poster2 = Poster.objects.create(
            submitter_name="Second User",
            image=self.create_test_image()
        )
        Poster.objects.create(
            submitter_name="Third User",
            image=self.create_test_image()
        )

        client = Client(HTTP_HOST='merch.localhost')
        response = client.get(
            f'/poster-gallery/{poster2.id}/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        data = response.json()
        self.assertEqual(len(data['posters']), 3)

        selected = data['posters'][data['initial_index']]
        self.assertEqual(selected['id'], poster2.id)
        self.assertEqual(selected['submitter_name'], 'Second User')

        self.assertCountEqual(
            [p['submitter_name'] for p in data['posters']],
            ['Test User', 'Second User', 'Third User'],
        )

    def test_wrap_around_navigation(self):
        """All posters are present so the client can wrap around either end."""
        poster2 = Poster.objects.create(
            submitter_name="Last User",
            image=self.create_test_image()
        )

        client = Client(HTTP_HOST='merch.localhost')
        response = client.get(
            f'/poster-gallery/{poster2.id}/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        data = response.json()
        self.assertEqual(len(data['posters']), 2)
        self.assertEqual(data['posters'][data['initial_index']]['id'], poster2.id)
        self.assertCountEqual(
            [p['submitter_name'] for p in data['posters']],
            ['Test User', 'Last User'],
        )

    def test_mobile_responsive_features(self):
        """Test that mobile-responsive features are present in the HTML"""
        client = Client(HTTP_HOST='merch.localhost')
        response = client.get('/peelitback2025poster/')
        content = response.content.decode()
        
        # Check for mobile viewport meta tag
        self.assertIn('user-scalable=yes', content)
        
        # Check for responsive image attributes
        self.assertIn('srcset=', content)
        self.assertIn('sizes=', content)
        
        # Check for lazy loading
        self.assertIn('loading="lazy"', content)
        
        # Check for external CSS and JS files
        self.assertIn('/static/merch/css/posters.css', content)
        self.assertIn('/static/merch/js/posters.js', content)



class StaticReferenceTestCase(TestCase):
    def test_static_references_resolve(self):
        """Every {% static %} path must be one collectstatic puts in the manifest.

        Tests run without the manifest, and the plain storage strips a leading
        slash, so a bad path renders fine here and 500s only in production.
        """
        pattern = re.compile(r"""{%\s*static\s+["']([^"']+)["']""")
        for template in Path(settings.BASE_DIR).glob('*/templates/**/*.html'):
            for path in pattern.findall(template.read_text()):
                with self.subTest(template=template.name, path=path):
                    self.assertFalse(path.startswith('/'))
                    self.assertIsNotNone(finders.find(path))


class RecentlyAddedTestCase(TestCase):
    """Issue #88: the index lists the newest products under the search bar."""

    def setUp(self):
        from merch.models import Category, Product

        self.client = Client(HTTP_HOST='merch.localhost')
        self.category = Category.objects.create(name='Shirts', tag='shirts')
        self.products = []
        for n in range(7):
            product = Product.objects.create(name=f'Shirt {n}', description='')
            product.categories.add(self.category)
            self.products.append(product)
        # The newest product is unauthorized and must not be shown.
        self.products[-1].is_authorized = 'N'
        self.products[-1].save()

    def test_shows_five_newest_authorized_products_newest_first(self):
        resp = self.client.get('/')
        self.assertEqual(
            [p.name for p in resp.context['recent_products']],
            ['Shirt 5', 'Shirt 4', 'Shirt 3', 'Shirt 2', 'Shirt 1'],
        )

    def test_section_follows_search_bar_and_links_to_products(self):
        html = self.client.get('/').content.decode()
        self.assertIn('Recently Added', html)
        self.assertLess(html.index('search-form'), html.index('Recently Added'))
        newest = self.products[5]
        self.assertIn(f'href="/shirts/{newest.tag()}/"', html)
        self.assertNotIn(self.products[6].tag(), html)

    def test_section_hidden_when_no_products(self):
        from merch.models import Product

        Product.objects.all().delete()
        self.assertNotContains(self.client.get('/'), 'Recently Added')


class LinkPreviewTestCase(TestCase):
    """Issue #57: merch pages carry Open Graph tags so shared links unfurl well."""

    def setUp(self):
        from merch.models import Category, Product, ProductImage

        self.client = Client(HTTP_HOST='merch.localhost')
        self.category = Category.objects.create(name='Shirts', tag='shirts')
        self.product = Product.objects.create(
            name='Devil T-Shirt',
            description='**Front** print with the devil.\n\n' + 'Long text. ' * 40,
        )
        self.product.categories.add(self.category)
        # Like most merch photos: a transparent PNG with the product in the
        # middle. Created second so the test proves order, not insertion, wins.
        ProductImage.objects.create(
            product=self.product, order=2,
            original=SimpleUploadedFile('blue.png', self.png((0, 0, 255, 255))),
        )
        shirt = Image.new('RGBA', (600, 600), (0, 0, 0, 0))
        shirt.paste((255, 0, 0, 255), (200, 200, 400, 400))
        ProductImage.objects.create(
            product=self.product, order=1,
            original=SimpleUploadedFile('red.png', self.png(image=shirt)),
        )

    def png(self, color=None, image=None):
        image = image or Image.new('RGBA', (600, 600), color)
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        return buf.getvalue()

    def meta(self, resp, prop):
        html = resp.content.decode()
        match = re.search(
            rf'<meta (?:property|name)="{re.escape(prop)}" content="([^"]*)"', html
        )
        return match and match.group(1)

    def test_product_page_previews_first_image(self):
        resp = self.client.get(f'/shirts/{self.product.tag()}/')
        first = self.product.productimage_set.first()
        self.assertEqual(first.order, 1)
        self.assertEqual(
            self.meta(resp, 'og:image'), f'http://merch.localhost{first.preview.url}'
        )
        self.assertEqual(self.meta(resp, 'twitter:card'), 'summary_large_image')
        self.assertEqual(self.meta(resp, 'og:title'), 'Devil T-Shirt')

    def test_preview_image_fills_transparency_with_black(self):
        first = self.product.productimage_set.first()
        first.preview.generate()
        with first.preview.storage.open(first.preview.name) as f:
            preview = Image.open(f)
            preview.load()
        self.assertEqual(preview.format, 'JPEG')
        self.assertEqual(preview.mode, 'RGB')
        w, h = preview.size
        corner = preview.getpixel((0, 0))
        centre = preview.getpixel((w // 2, h // 2))
        self.assertTrue(all(c < 16 for c in corner), corner)
        self.assertGreater(centre[0], 200)
        self.assertTrue(centre[1] < 60 and centre[2] < 60, centre)

    def test_product_description_is_plain_and_short(self):
        resp = self.client.get(f'/shirts/{self.product.tag()}/')
        description = self.meta(resp, 'og:description')
        self.assertTrue(description.startswith('Front print with the devil.'))
        self.assertNotIn('<', description)
        self.assertLessEqual(len(description), 200)

    def test_index_describes_the_site(self):
        resp = self.client.get('/')
        self.assertEqual(self.meta(resp, 'og:site_name'), 'merch.nincatalog.com')
        self.assertIn('merchandise', self.meta(resp, 'og:description'))
        self.assertEqual(self.meta(resp, 'twitter:card'), 'summary')
