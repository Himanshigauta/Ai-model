import pandas as pd
import numpy as np
import sqlite3
import os
from datasets import load_dataset

def clean_rate(rate_str):
    if pd.isna(rate_str):
        return 0.0
    rate_str = str(rate_str).strip()
    if rate_str == '-' or rate_str == 'NEW':
        return 0.0
    try:
        # e.g., '4.1/5' -> 4.1
        return float(rate_str.split('/')[0])
    except:
        return 0.0

def clean_cost(cost_str):
    if pd.isna(cost_str):
        return 0
    cost_str = str(cost_str).replace(',', '').strip()
    try:
        return int(cost_str)
    except:
        return 0

def clean_data(df):
    """Clean the zomato dataset."""
    df_clean = df.copy()
    
    # 1. Clean rating
    if 'rate' in df_clean.columns:
        df_clean['rating'] = df_clean['rate'].apply(clean_rate)
    
    # 2. Clean cost
    if 'approx_cost(for two people)' in df_clean.columns:
        df_clean['cost'] = df_clean['approx_cost(for two people)'].apply(clean_cost)
    
    # 3. Handle missing values in text columns
    text_cols = ['name', 'address', 'location', 'rest_type', 'cuisines', 'listed_in(type)']
    for col in text_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('Unknown')
    
    # Select final columns we care about for the recommendation engine
    keep_cols = [
        'name', 'url', 'address', 'location', 'rest_type', 
        'cuisines', 'rating', 'votes', 'cost', 'listed_in(type)'
    ]
    
    # Only keep columns that actually exist
    keep_cols = [c for c in keep_cols if c in df_clean.columns]
    
    return df_clean[keep_cols]

def load_and_preprocess(dataset_name="ManikaSaini/zomato-restaurant-recommendation", db_path="zomato.db"):
    print("Downloading dataset...")
    ds = load_dataset(dataset_name, split='train')
    df = ds.to_pandas()
    
    print("Cleaning data...")
    df_clean = clean_data(df)
    
    print(f"Saving cleaned data ({len(df_clean)} rows) to SQLite database: {db_path}...")
    conn = sqlite3.connect(db_path)
    df_clean.to_sql('restaurants', conn, if_exists='replace', index=False)
    conn.close()
    
    print("Data preprocessing completed successfully.")
    return df_clean

if __name__ == "__main__":
    db_file = os.path.join(os.path.dirname(__file__), "zomato_cleaned.db")
    load_and_preprocess(db_path=db_file)
