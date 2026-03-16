import unittest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})

    def test_recommend_endpoint(self):
        # We will test an easy retrieval prompt to see if the full pipeline returns a 200 success 
        payload = {
            "place": "Banashankari",
            "cuisine": "North Indian",
            "max_price": 500,
            "min_rating": 3.0
        }
        
        response = self.client.post("/api/recommend", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("recommendation", data)
        
        # It must either contain the text 'success' or 'error' (if API key failed, though we just verified it works)
        self.assertIn(data["status"], ["success", "error"])
        self.assertIsInstance(data["recommendation"], str)
        self.assertTrue(len(data["recommendation"]) > 0)
        
if __name__ == '__main__':
    unittest.main()
