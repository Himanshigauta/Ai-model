import unittest
import os
from dotenv import load_dotenv
from llm_agent import construct_prompt, generate_recommendation

# Load the API key from .env file
load_dotenv()

class TestLLMAgentIntegration(unittest.TestCase):
    
    def test_construct_prompt_no_results(self):
        prefs = {"place": "Nowhere"}
        docs = []
        prompt = construct_prompt(prefs, docs)
        self.assertIn("no matching restaurants were found", prompt)
        
    def test_construct_prompt_with_results(self):
        prefs = {"place": "Indiranagar", "cuisine": "Chinese"}
        docs = [
            {
                "name": "Super Dragon",
                "rating": 4.5,
                "votes": 120,
                "cost": 800,
                "cuisines": "Chinese, Asian",
                "location": "Indiranagar",
                "address": "123 Main St"
            }
        ]
        prompt = construct_prompt(prefs, docs)
        self.assertIn("Super Dragon", prompt)
        self.assertIn("Indiranagar", prompt)
        self.assertIn("Chinese", prompt)
        self.assertIn("4.5", prompt)

    def test_live_groq_api_call(self):
        """
        Integration test that actually hits the Groq API.
        This test will fail if the API key is not valid or if there are network issues.
        """
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            self.skipTest("GROQ_API_KEY is not set. Skipping live API test.")
            
        test_prompt = "Say the word 'success' and nothing else."
        
        # Use a faster, smaller model for testing
        response = generate_recommendation(test_prompt, model="llama-3.1-8b-instant")
        
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)
        self.assertNotIn("Error", response)
        self.assertIn("success", response.lower())

if __name__ == '__main__':
    unittest.main()
