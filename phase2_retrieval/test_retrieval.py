import unittest
import os
import sqlite3
import pandas as pd
from retrieval import get_recommendations

class TestRetrievalEngine(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up a temporary mock database for testing."""
        cls.db_path = "test_zomato_mock.db"
        conn = sqlite3.connect(cls.db_path)
        
        # Mock data
        data = {
            "name": ["Cheap Pizza", "Fancy Pizza", "Good Indian", "Bad Indian", "Great Chinese"],
            "address": ["Address 1", "Address 2", "Banashankari Road", "Somewhere", "Address 3"],
            "location": ["Banashankari", "Indiranagar", "Banashankari", "Banashankari", "Koramangala"],
            "rest_type": ["Quick Bites", "Casual Dining", "Casual Dining", "Quick Bites", "Casual Dining"],
            "cuisines": ["Italian, Pizza", "Italian, Pizza", "North Indian, South Indian", "North Indian", "Chinese"],
            "rating": [3.5, 4.5, 4.2, 2.5, 4.8],
            "votes": [100, 500, 300, 10, 800],
            "cost": [400, 2500, 800, 300, 1200],
            "listed_in(type)": ["Delivery", "Dine-out", "Dine-out", "Delivery", "Dine-out"]
        }
        
        df = pd.DataFrame(data)
        df.to_sql('restaurants', conn, if_exists='replace', index=False)
        conn.close()

    @classmethod
    def tearDownClass(cls):
        """Clean up the mock database after tests."""
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)

    def test_filter_by_place(self):
        df = get_recommendations(self.db_path, place="Banashankari")
        # Should return 'Cheap Pizza', 'Good Indian', 'Bad Indian'
        self.assertEqual(len(df), 3)
        names = df['name'].tolist()
        self.assertIn("Cheap Pizza", names)
        self.assertIn("Good Indian", names)
        
    def test_filter_by_cuisine(self):
        df = get_recommendations(self.db_path, cuisine="Pizza")
        self.assertEqual(len(df), 2)
        names = df['name'].tolist()
        self.assertIn("Cheap Pizza", names)
        
    def test_filter_by_price(self):
        df = get_recommendations(self.db_path, max_price=500)
        self.assertEqual(len(df), 2)
        
    def test_filter_by_rating(self):
        df = get_recommendations(self.db_path, min_rating=4.5)
        # Should return Fancy Pizza (4.5) and Great Chinese (4.8)
        self.assertEqual(len(df), 2)
        
    def test_combined_filters(self):
        df = get_recommendations(
            self.db_path, 
            place="Banashankari", 
            cuisine="Indian", 
            min_rating=4.0
        )
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['name'], "Good Indian")

    def test_top_n_limit(self):
        df = get_recommendations(self.db_path, place="Banashankari", top_n=2)
        self.assertEqual(len(df), 2)
        # Verify it's sorted by highest rating first
        self.assertEqual(df.iloc[0]['name'], "Good Indian")

if __name__ == '__main__':
    unittest.main()
