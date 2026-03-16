import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the module directory (.env)
from pathlib import Path
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path)

def construct_prompt(user_preferences, retrieved_restaurants):
    """
    Constructs a detailed prompt for the LLM based on user preferences and context.
    
    Args:
        user_preferences (dict): Dictionary of user filters (e.g., {'place': 'Banashankari', 'cuisine': 'Pizza'})
        retrieved_restaurants (list): List of dictionaries containing restaurant details.
        
    Returns:
        str: The fully constructed prompt ready to be sent to the LLM.
    """
    
    if not retrieved_restaurants:
        return (
            f"The user was looking for restaurants with these preferences: {user_preferences}. "
            "However, no matching restaurants were found in the database. "
            "Please write a polite response apologizing that no exact matches could be found, "
            "and perhaps suggest they widen their search criteria."
        )

    prompt = f"You are an expert food and restaurant recommendation assistant.\n\n"
    prompt += f"A user is asking for recommendations with the following preferences:\n"
    for key, val in user_preferences.items():
        if val:
            prompt += f"- {key.capitalize()}: {val}\n"
            
    prompt += "\nHere are the top restaurant matches retrieved from our verified database:\n"
    
    for i, r in enumerate(retrieved_restaurants, 1):
        prompt += f"\n--- Restaurant {i} ---\n"
        prompt += f"Name: {r.get('name', 'N/A')}\n"
        prompt += f"Rating: {r.get('rating', 'N/A')} stars (from {r.get('votes', 0)} votes)\n"
        prompt += f"Cost for Two: {r.get('cost', 'N/A')} INR\n"
        prompt += f"Cuisines: {r.get('cuisines', 'N/A')}\n"
        prompt += f"Location: {r.get('location', 'N/A')}\n"
        prompt += f"Address: {r.get('address', 'N/A')}\n"
        
    prompt += (
        "\nBased on the above options, write a friendly recommendation for the user. "
        "However, you MUST return your response as a valid JSON object with the following exact structure and no other text:\n"
        "{\n"
        "  \"intro\": \"A friendly short 2-sentence introduction.\",\n"
        "  \"restaurants\": [\n"
        "      {\n"
        "          \"name\": \"Restaurant Name\",\n"
        "          \"rating\": \"Numeric rating (e.g. 4.5)\",\n"
        "          \"cost\": \"Approx cost for two (e.g. 600)\",\n"
        "          \"location\": \"Area name\",\n"
        "          \"cuisine\": \"Primary cuisines\",\n"
        "          \"reason\": \"A 2-sentence punchy reason why it is recommended based on their preferences.\"\n"
        "      }\n"
        "  ],\n"
        "  \"outro\": \"A friendly 1-sentence closing.\"\n"
        "}"
    )
    
    return prompt


import streamlit as st

def generate_recommendation(prompt, model="llama-3.3-70b-versatile"):
    """
    Calls the Groq LLM API to generate the final recommendation.
    
    Args:
        prompt (str): The constructed prompt string.
        model (str): The Groq model to use.
        
    Returns:
        str: The generated text response.
    """
    
    # Try getting key from streamlit secrets (for deployment) or environment (local)
    api_key = None
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except:
        pass
        
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY")
        
    if not api_key:
        return "Error: GROQ_API_KEY not found in Streamlit Secrets or Environment Variables. Please set it to proceed."
        
    client = Groq(api_key=api_key)
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful JSON-only API. You must output only strictly valid JSON and no conversational filler."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=1024,
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"An error occurred while calling the Groq API: {str(e)}"

# Example usage (will only execute successfully if GROQ_API_KEY is available in environment)
if __name__ == "__main__":
    prefs = {"place": "Indiranagar", "cuisine": "Chinese", "max_price": 1000}
    docs = [
        {
            "name": "Super Dragon",
            "rating": 4.5,
            "votes": 120,
            "cost": 800,
            "cuisines": "Chinese, Asian",
            "location": "Indiranagar",
            "address": "123 Main St, Indiranagar"
        }
    ]
    
    p = construct_prompt(prefs, docs)
    print("--- Prompt ---")
    print(p)
    print("\n--- Response ---")
    print(generate_recommendation(p))
