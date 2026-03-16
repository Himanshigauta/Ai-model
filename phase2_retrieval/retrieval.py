import sqlite3
import pandas as pd
import os

def get_recommendations(
    db_path,
    place=None,
    cuisine=None,
    max_price=None,
    min_rating=None,
    top_n=5
):
    """
    Query the SQLite database for restaurants matching the user's constraints.
    
    Args:
        db_path (str): Path to the SQLite DB.
        place (str): Location of the restaurant (substring match).
        cuisine (str): Cuisine type (substring match).
        max_price (int): Maximum cost for two people.
        min_rating (float): Minimum acceptable rating.
        top_n (int): Number of top results to return.
        
    Returns:
        pd.DataFrame: DataFrame containing top N matching restaurants sorted by rating and cost.
    """
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}. Please run Phase 1 preprocessing first.")
    
    conn = sqlite3.connect(db_path)
    
    # Base query
    query = "SELECT * FROM restaurants WHERE 1=1"
    params = []
    
    if place:
        # Check either exactly in location or addresses containing place
        query += " AND (location LIKE ? OR address LIKE ?)"
        params.extend([f"%{place}%", f"%{place}%"])
        
    if cuisine:
        query += " AND cuisines LIKE ?"
        params.append(f"%{cuisine}%")
        
    if max_price is not None:
        query += " AND cost > 0 AND cost <= ?"
        params.append(max_price)
        
    if min_rating is not None:
        query += " AND rating >= ?"
        params.append(min_rating)
        
    # Sort first by highest rating, then lowest cost
    query += " ORDER BY rating DESC, cost ASC"
    
    if top_n is not None:
        query += " LIMIT ?"
        params.append(top_n)
        
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    return df

if __name__ == "__main__":
    db_file = os.path.join(os.path.dirname(__file__), "..", "phase1_data_pipeline", "zomato_cleaned.db")
    
    print("Testing manual retrieval...")
    results = get_recommendations(
        db_path=db_file, 
        place="Banashankari", 
        cuisine="North Indian", 
        max_price=1000, 
        min_rating=4.0, 
        top_n=3
    )
    
    if not results.empty:
        print(f"Got {len(results)} results:")
        for idx, row in results.iterrows():
            print(f"- {row['name']} ({row['rating']} stars, Cost: {row['cost']}) | Cuisines: {row['cuisines']}")
    else:
        print("No results found.")
