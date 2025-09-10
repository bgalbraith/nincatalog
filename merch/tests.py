from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

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

    def test_poster_gallery_view(self):
        """Test the poster gallery view loads"""
        client = Client(HTTP_HOST='merch.localhost')
        response = client.get(f'/poster-gallery/{self.poster.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")

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
        """Test gallery with multiple posters"""
        # Create additional posters
        poster2 = Poster.objects.create(
            submitter_name="Second User",
            image=self.create_test_image()
        )
        poster3 = Poster.objects.create(
            submitter_name="Third User", 
            image=self.create_test_image()
        )
        
        client = Client(HTTP_HOST='merch.localhost')
        # Test clicking on the second poster
        response = client.get(
            f'/poster-gallery/{poster2.id}/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        data = response.json()
        self.assertEqual(len(data['posters']), 3)  # All 3 posters
        self.assertEqual(data['initial_index'], 1)  # Second poster (0-indexed)
        self.assertEqual(data['posters'][1]['submitter_name'], 'Second User')

    def test_wrap_around_navigation(self):
        """Test that gallery supports wrap-around navigation logic"""
        # Create additional posters to test wrap-around
        poster2 = Poster.objects.create(
            submitter_name="Last User",
            image=self.create_test_image()
        )
        
        client = Client(HTTP_HOST='merch.localhost')
        # Test clicking on the last poster
        response = client.get(
            f'/poster-gallery/{poster2.id}/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        data = response.json()
        self.assertEqual(len(data['posters']), 2)  # Two posters total
        self.assertEqual(data['initial_index'], 1)  # Last poster (0-indexed)
        
        # Verify all posters are accessible for wrap-around
        self.assertEqual(data['posters'][0]['submitter_name'], 'Test User')
        self.assertEqual(data['posters'][1]['submitter_name'], 'Last User')

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
