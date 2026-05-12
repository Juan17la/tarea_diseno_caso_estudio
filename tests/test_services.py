import unittest
import os
from unittest.mock import patch, MagicMock
from utils.validator import URLValidator
from services.extractor_service import ExtractorService
from services.image_service import ImageService
from PIL import ImageTk

class TestURLValidator(unittest.TestCase):
    def setUp(self):
        self.validator = URLValidator()

    def test_valid_youtube_urls(self):
        urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ"
        ]
        for url in urls:
            is_valid, error = self.validator.validate(url)
            self.assertTrue(is_valid, f"URL should be valid: {url}")
            self.assertIsNone(error)

    def test_valid_twitter_urls(self):
        urls = [
            "https://twitter.com/user/status/123456789",
            "https://x.com/user/status/123456789"
        ]
        for url in urls:
            is_valid, error = self.validator.validate(url)
            self.assertTrue(is_valid, f"URL should be valid: {url}")
            self.assertIsNone(error)

    def test_valid_instagram_urls(self):
        urls = [
            "https://www.instagram.com/p/CXYZ1234/"
        ]
        for url in urls:
            is_valid, error = self.validator.validate(url)
            self.assertTrue(is_valid, f"URL should be valid: {url}")
            self.assertIsNone(error)

    def test_invalid_urls(self):
        urls = [
            "https://www.google.com",
            "ftp://youtube.com/watch",
            "not a url",
            ""
        ]
        for url in urls:
            is_valid, error = self.validator.validate(url)
            self.assertFalse(is_valid, f"URL should be invalid: {url}")
            self.assertIsNotNone(error)

class TestExtractorService(unittest.TestCase):
    def setUp(self):
        self.service = ExtractorService()

    def test_fetch_info_invalid_url(self):
        with self.assertRaises(ValueError):
            self.service.fetch_info("https://www.google.com")
            
    def test_normalize_progress_data(self):
        # Test progress hook normalization correctly processes data
        data = {
            "status": "downloading",
            "downloaded_bytes": 500,
            "total_bytes": 1000
        }
        normalized = self.service._normalize_progress_data(data)
        self.assertEqual(normalized["progress"], 50.0)
        self.assertEqual(normalized["status"], "downloading")
        
        data_finished = {"status": "finished"}
        normalized_finished = self.service._normalize_progress_data(data_finished)
        self.assertEqual(normalized_finished["progress"], 100.0)

    @patch("services.extractor_service.yt_dlp.YoutubeDL")
    def test_download_progress_hook(self, mock_ydl_class):
        mock_instance = mock_ydl_class.return_value.__enter__.return_value
        mock_instance.extract_info.return_value = {"title": "Test Video"}
        
        hook_called = False
        def dummy_hook(progress, data):
            nonlocal hook_called
            hook_called = True
            
        self.service.download(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
            "output.mp4", 
            "mp4", 
            dummy_hook
        )
        
        mock_instance.extract_info.assert_called_once()
        
class TestImageService(unittest.TestCase):
    def setUp(self):
        self.service = ImageService()

    @patch("tkinter.Tk")
    def test_load_from_url(self, mock_tk):
        # Tkinter requires a root window for PhotoImage. Since we're in a headless 
        # test environment, we patch Tk or handle the error gracefully if it fails
        # just for this test, but let's test with a real URL and check the instance.
        
        real_url = "https://picsum.photos/200"
        
        try:
            # We mock ImageTk.PhotoImage just to avoid the "RuntimeError: Too early to create image"
            # error in headless environments when no Tk instance exists.
            with patch("services.image_service.ImageTk.PhotoImage") as mock_photoimage:
                result = self.service.load_from_url(real_url)
                mock_photoimage.assert_called_once()
        except ValueError as e:
            self.fail(f"load_from_url raised ValueError unexpectedly: {e}")

if __name__ == "__main__":
    unittest.main()
