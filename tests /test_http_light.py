import unittest
import urllib.request
import os

ENV = os.environ.get("ENVIRONMENT", "dev").lower()
if ENV == "prod":
    BASE_URL = "http://10.48.229.153"  # or your prod LB IP if you changed it
else:
    BASE_URL = "http://127.0.0.1:5000"  # Dev ClusterIP via port-forward

class HttpLightTests(unittest.TestCase):

    def test_index_page_loads(self):
        """Check that the index page returns 200"""
        with urllib.request.urlopen(BASE_URL) as response:
            self.assertEqual(response.status, 200)

    def test_sample_book_exists(self):
        """Check that a known sample or test book exists in the HTML"""
        with urllib.request.urlopen(BASE_URL) as response:
            html = response.read().decode('utf-8')
        sample_books = ["Test Book 0", "The DevOps Handbook", "Python Crash Course"]
        found = any(book in html for book in sample_books)
        self.assertTrue(found, "No sample books found in the page source")

if __name__ == "__main__":
    unittest.main()
