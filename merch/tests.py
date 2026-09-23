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
