import streamlit as st
import json
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# Load local .env if it exists
load_dotenv()
load_dotenv(Path(__file__).parent / "phase3_llm_integration" / ".env")

# Import direct logic modules
from phase2_retrieval.retrieval import get_recommendations
from phase3_llm_integration.llm_agent import construct_prompt, generate_recommendation

# --- Page Configuration ---
st.set_page_config(
    page_title="Zomato AI - Sixth Sense",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LOCATIONS = ['BTM', 'Banashankari', 'Banaswadi', 'Bannerghatta Road', 'Basavanagudi', 'Basaveshwara Nagar', 'Bellandur', 'Bommanahalli', 'Brigade Road', 'Brookefield', 'CV Raman Nagar', 'Central Bangalore', 'Church Street', 'City Market', 'Commercial Street', 'Cunningham Road', 'Domlur', 'East Bangalore', 'Ejipura', 'Electronic City', 'Frazer Town', 'HBR Layout', 'HSR', 'Hebbal', 'Hennur', 'Hosur Road', 'ITPL Main Road, Whitefield', 'Indiranagar', 'Infantry Road', 'JP Nagar', 'Jakkur', 'Jalahalli', 'Jayanagar', 'Jeevan Bhima Nagar', 'KR Puram', 'Kaggadasapura', 'Kalyan Nagar', 'Kammanahalli', 'Kanakapura Road', 'Kengeri', 'Koramangala', 'Koramangala 1st Block', 'Koramangala 2nd Block', 'Koramangala 3rd Block', 'Koramangala 4th Block', 'Koramangala 5th Block', 'Koramangala 6th Block', 'Koramangala 7th Block', 'Koramangala 8th Block', 'Kumaraswamy Layout', 'Langford Town', 'Lavelle Road', 'MG Road', 'Magadi Road', 'Majestic', 'Malleshwaram', 'Marathahalli', 'Mysore Road', 'Nagarbhavi', 'Nagawara', 'New BEL Road', 'North Bangalore', 'Old Airport Road', 'Old Madras Road', 'Peenya', 'RT Nagar', 'Race Course Road', 'Rajajinagar', 'Rajarajeshwari Nagar', 'Rammurthy Nagar', 'Residency Road', 'Richmond Road', 'Sadashiv Nagar', 'Sahakara Nagar', 'Sanjay Nagar', 'Sankey Road', 'Sarjapur Road', 'Seshadripuram', 'Shanti Nagar', 'Shivajinagar', 'South Bangalore', 'St. Marks Road', 'Thippasandra', 'Ulsoor', 'Unknown', 'Uttarahalli', 'Varthur Main Road, Whitefield', 'Vasanth Nagar', 'Vijay Nagar', 'West Bangalore', 'Whitefield', 'Wilson Garden', 'Yelahanka', 'Yeshwantpur']
CUISINES = ['Afghan', 'Afghani', 'African', 'American', 'Andhra', 'Arabian', 'Asian', 'Assamese', 'Australian', 'Awadhi', 'BBQ', 'Bakery', 'Bar Food', 'Belgian', 'Bengali', 'Beverages', 'Bihari', 'Biryani', 'Bohri', 'British', 'Bubble Tea', 'Burger', 'Burmese', 'Cafe', 'Cantonese', 'Charcoal Chicken', 'Chettinad', 'Chinese', 'Coffee', 'Continental', 'Desserts', 'Drinks Only', 'European', 'Fast Food', 'Finger Food', 'French', 'German', 'Goan', 'Greek', 'Grill', 'Gujarati', 'Healthy Food', 'Hot dogs', 'Hyderabadi', 'Ice Cream', 'Indian', 'Indonesian', 'Iranian', 'Italian', 'Japanese', 'Jewish', 'Juices', 'Kashmiri', 'Kebab', 'Kerala', 'Konkan', 'Korean', 'Lebanese', 'Lucknowi', 'Maharashtrian', 'Malaysian', 'Malwani', 'Mangalorean', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Mithai', 'Modern Indian', 'Momos', 'Mongolian', 'Mughlai', 'Naga', 'Nepalese', 'North Eastern', 'North Indian', 'Oriya', 'Paan', 'Pan Asian', 'Parsi', 'Pizza', 'Portuguese', 'Rajasthani', 'Raw Meats', 'Roast Chicken', 'Rolls', 'Russian', 'Salad', 'Sandwich', 'Seafood', 'Sindhi', 'Singaporean', 'South American', 'South Indian', 'Spanish', 'Sri Lankan', 'Steak', 'Street Food', 'Sushi', 'Tamil', 'Tea', 'Tex-Mex', 'Thai', 'Tibetan', 'Turkish', 'Unknown', 'Vegan', 'Vietnamese', 'Wraps']

st.markdown(f"<style>/* Cache Buster: {time.time()} */</style>", unsafe_allow_html=True)
st.markdown("""
<style>
    /* Full Page Zomato Red Background */
    .stApp {
        background-color: #E23744 !important; /* Authentic Zomato Red */
        color: #FFFFFF !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Global Text Contrast */
    h1, h2, h3, p, label, .stMarkdown {
        color: #FFFFFF !important;
    }
    
    /* Hero Typography */
    .hero-title {
        font-size: 60px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 20px;
        color: #FFFFFF;
        letter-spacing: -1.5px;
    }
    .hero-title span {
        color: #FFFFFF;
    }
    .hero-sub {
        font-size: 18px;
        color: rgba(255, 255, 255, 0.9);
        max-width: 600px;
        line-height: 1.5;
        margin-bottom: 40px;
    }
    
    /* Input Search Bar and Sliders */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background: #FFFFFF !important;
        color: #333333 !important;
        border-radius: 12px !important;
        border: 2px solid #FFFFFF !important;
        padding: 12px 18px !important;
        font-size: 15px !important;
    }
    .stSlider > div[data-baseweb="slider"] {
        padding-top: 15px;
    }
    [data-testid="stThumbValue"] {
        color: #FFFFFF !important;
    }

    /* Primary Premium Dark Button */
    .stButton>button {
        background: #1a1a1a !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 0.8rem 2.8rem !important;
        transition: all 0.3s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 20px rgba(226, 55, 68, 0.4) !important;
        margin-top: 10px;
        text-transform: none;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(226, 55, 68, 0.6) !important;
        border: 1px solid rgba(226, 55, 68, 0.5) !important;
    }
    
    /* Detailed Card Buttons */
    .action-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-decoration: none !important;
        font-weight: 700;
        font-size: 0.85em;
        padding: 8px 16px;
        border-radius: 10px;
        transition: all 0.2s ease;
        flex: 1;
        text-align: center;
    }
    .btn-maps { background: #E23744; color: white !important; }
    .btn-maps:hover { background: #c32f3a; transform: scale(1.05); }
    .btn-outline { border: 1px solid rgba(255,255,255,0.3); color: white !important; }
    .btn-outline:hover { background: rgba(255,255,255,0.1); border-color: white; }
    
    /* Vertical Flex Container for Cards */
    .card-container {
        display: flex;
        flex-direction: column;
        gap: 25px;
        padding: 20px 0;
        margin-top: 10px;
        align-items: center;
    }
    
    .card-container::-webkit-scrollbar {
        display: none;
    }
    
    /* Recommendation Card (Premium Dark Glassmorphism) */
    .recommendation-card {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        color: #FFFFFF !important;
        width: 100%;
        max-width: 800px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease;
    }
    .recommendation-card:hover {
        transform: scale(1.01);
    }
    
    .card-header h3 {
        color: #FFFFFF !important;
        margin-bottom: 4px;
        font-size: 1.5em;
        font-weight: 800;
        border: none !important;
        padding-bottom: 0 !important;
    }
    .card-meta {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    
    .card-stats {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
        font-size: 0.9em;
    }
    .stat-badge {
        display: flex;
        align-items: center;
        gap: 4px;
        color: #FFD700;
        font-weight: bold;
    }
    .stat-price {
        color: rgba(255, 255, 255, 0.8);
    }
    
    .ai-why-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .ai-why-label {
        font-size: 0.75em;
        font-weight: 900;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        margin-bottom: 8px;
        display: block;
    }
    .ai-why-text {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9em;
        line-height: 1.5;
    }
    
    .card-actions {
        display: flex;
        gap: 10px;
        margin-top: auto;
    }
    
    .globe-img {
        width: 100%;
        max-width: 550px;
        margin-top: 40px;
        filter: drop-shadow(0 0 40px rgba(226, 55, 68, 0.3));
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
</style>
""", unsafe_allow_html=True)

# --- Top Nav ---
st.markdown("""
<div style="padding: 20px 0; margin-bottom: 40px; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 28px; font-weight: 800; font-style: italic; letter-spacing: -1px;">zomato</div>
    <div style="font-weight: 500; font-size: 14px; opacity: 0.8;">Curated by AI</div>
</div>
""", unsafe_allow_html=True)

# --- Main Layout ---
left_col, right_col = st.columns([1.3, 1])

with left_col:
    st.markdown("""
    <div class="hero-title">
        Zomato AI -<br>
        <span>Your Sixth Sense</span> for<br>
        Exceptional Dining
    </div>
    <div class="hero-sub">
        Artificial Intelligence meets Human Intuition. Discover the flawless restaurants specifically tailored to your precise craving instantly, backed by thousands of real Zomato reviews.
    </div>
    """, unsafe_allow_html=True)
    
    col_A, col_B = st.columns(2)
    with col_A:
        place = st.selectbox("📍 Target Location", [""] + LOCATIONS, index=0)
    with col_B:
        cuisine = st.selectbox("🍜 Cravings (Cuisine)", [""] + CUISINES, index=0)
        
    col_C, col_D = st.columns(2)
    with col_C:
        price_opts = {"Budget (<500)": 500, "Mid-range (<1000)": 1000, "Fine Dining (<2500)": 2500, "Any": None}
        selected_price = st.selectbox("💰 Max Spending (Two)", list(price_opts.keys()))
        max_price = price_opts[selected_price]
        
    with col_D:
        min_rating = st.slider("⭐ Minimum Acceptable Rating", min_value=1.0, max_value=5.0, value=3.9, step=0.1)

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.button("Uncover Restaurants")

with right_col:
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://images.unsplash.com/photo-1550989460-0adf9ea622e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=700&q=80" 
             style="border-radius: 50%; object-fit: cover; width: 450px; height: 450px;" class="globe-img">
    </div>
    """, unsafe_allow_html=True)

# --- Response Area ---
if submit:
    if not place and not cuisine:
        st.warning("Please enter at least a Location or Cuisine to see the magic happen.")
    else:
        with st.spinner("Synchronizing neural nodes with Zomato datasets..."):
            # Direct logic integration instead of API call
            db_path = Path(__file__).parent / "phase1_data_pipeline" / "zomato_cleaned.db"
            
            try:
                # 1. Retrieval
                df = get_recommendations(
                    db_path=str(db_path),
                    place=place if place else None,
                    cuisine=cuisine if cuisine else None,
                    max_price=max_price,
                    min_rating=float(min_rating),
                    top_n=8
                )
                retrieved_docs = df.to_dict('records')
                
                if not retrieved_docs:
                    st.warning("Oops! We couldn't find any recommendations matching your criteria.")
                    st.stop()
                
                # 2. Prompt & LLM
                user_prefs = {
                    "place": place,
                    "cuisine": cuisine,
                    "max_price": max_price,
                    "min_rating": float(min_rating)
                }
                prompt = construct_prompt(user_prefs, retrieved_docs)
                response_text = generate_recommendation(prompt)
                
                # Clean LLM response (strip markdown codes if present)
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                
                if response_text.startswith("Error:"):
                    st.error(response_text)
                else:
                    try:
                        llm_json = json.loads(response_text)
                        
                        st.markdown(f'<div style="font-size: 1.1em; margin-bottom: 25px; color: #EAEAEA;">{llm_json.get("intro", "").strip()}</div>', unsafe_allow_html=True)
                        
                        ai_restaurants = llm_json.get("restaurants", [])
                        if ai_restaurants:
                            all_cards_html = ""
                            for ai_rec in ai_restaurants:
                                r_name = ai_rec.get("name", "Restaurant")
                                reason = ai_rec.get("reason", "")
                                r_rating = ai_rec.get("rating", "4.0")
                                r_cost = ai_rec.get("cost", "1000")
                                r_location = ai_rec.get("location", place if place else "Bangalore")
                                r_cuisine = ai_rec.get("cuisine", cuisine if cuisine else "Multi-Cuisine")
                                
                                url = "#"
                                for db_rest in retrieved_docs:
                                    if r_name.lower() in db_rest.get("name", "").lower():
                                        url = db_rest.get("url", "#")
                                        break
                                        
                                maps_url = f"https://www.google.com/maps/search/{r_name.replace(' ', '+')}+{r_location.replace(' ', '+')}"
                                
                                card_html = f"""
                                <div class="recommendation-card">
                                    <div class="card-header">
                                        <h3>{r_name}</h3>
                                        <div class="card-meta">{r_location} • {r_cuisine}</div>
                                    </div>
                                    <div class="card-stats">
                                        <div class="stat-badge">⭐ {r_rating}</div>
                                        <div class="stat-price">Approx ₹{r_cost} for two</div>
                                    </div>
                                    <div class="ai-why-section">
                                        <span class="ai-why-label">AI WHY</span>
                                        <div class="ai-why-text">{reason}</div>
                                    </div>
                                    <div class="card-actions">
                                        <a href="{maps_url}" target="_blank" class="action-btn btn-maps">📍 Open in Maps</a>
                                        <a href="{url}" target="_blank" class="action-btn btn-outline">View Menu</a>
                                    </div>
                                </div>
                                """
                                # Strip newlines to prevent markdown parser from breaking
                                all_cards_html += card_html.replace("\n", " ").strip()
                            
                            st.markdown(f'<div class="card-container">{all_cards_html}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div style="margin-top: 25px; font-style: italic; color: rgba(255,255,255,0.7);">{llm_json.get("outro", "").strip()}</div>', unsafe_allow_html=True)
                            st.balloons()
                            
                    except json.JSONDecodeError:
                        st.error("The AI returned an invalid format. Trying to show raw text:")
                        st.write(response_text)
                        
            except Exception as e:
                st.error(f"Failed to generate recommendation: {str(e)}")
