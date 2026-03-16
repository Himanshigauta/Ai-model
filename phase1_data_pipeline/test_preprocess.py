import unittest
import pandas as pd
from preprocess import clean_data, clean_rate, clean_cost

class TestDataPipeline(unittest.TestCase):
    def test_clean_rate(self):
        self.assertEqual(clean_rate("4.1/5"), 4.1)
        self.assertEqual(clean_rate("4.1 /5"), 4.1)
        self.assertEqual(clean_rate("NEW"), 0.0)
        self.assertEqual(clean_rate("-"), 0.0)
        self.assertEqual(clean_rate(float('nan')), 0.0)

    def test_clean_cost(self):
        self.assertEqual(clean_cost("800"), 800)
        self.assertEqual(clean_cost("1,200"), 1200)
        self.assertEqual(clean_cost(""), 0)
        self.assertEqual(clean_cost(float('nan')), 0)

    def test_clean_data_pipeline(self):
        # Create a mock dataframe
        data = {
            "name": ["Jalsa", None],
            "rate": ["4.1/5", "NEW"],
            "approx_cost(for two people)": ["800", "1,200"],
            "votes": [775, 10],
            "location": ["Banashankari", None]
        }
        df = pd.DataFrame(data)
        
        # Clean data
        df_clean = clean_data(df)
        
        # Assertions
        self.assertIn("rating", df_clean.columns)
        self.assertIn("cost", df_clean.columns)
        self.assertEqual(list(df_clean["rating"]), [4.1, 0.0])
        self.assertEqual(list(df_clean["cost"]), [800, 1200])
        self.assertEqual(list(df_clean["location"]), ["Banashankari", "Unknown"])
        self.assertEqual(list(df_clean["name"]), ["Jalsa", "Unknown"])

if __name__ == '__main__':
    unittest.main()
