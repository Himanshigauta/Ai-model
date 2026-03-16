import unittest
from unittest.mock import patch, MagicMock
from app import st
import requests

class TestUIIntegration(unittest.TestCase):
    
    @patch('requests.post')
    def test_successful_api_call(self, mock_post):
        # Mocking the backend API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "recommendation": "Here are 3 great pizza places..."
        }
        mock_post.return_value = mock_response
        
        # Test the request trigger
        payload = {
            "place": "Banashankari",
            "cuisine": "Pizza",
            "max_price": 1000,
            "min_rating": 4.0
        }
        
        response = requests.post("http://localhost:8000/api/recommend", json=payload)
        
        # Assert the network call occurred
        mock_post.assert_called_once_with("http://localhost:8000/api/recommend", json=payload)
        
        # Assert the UI logic handles the response cleanly
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("pizza", data["recommendation"].lower())

    @patch('requests.post')
    def test_api_connection_error(self, mock_post):
        # Mocking a server down scenario
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.post("http://localhost:8000/api/recommend", json={})

if __name__ == '__main__':
    unittest.main()
