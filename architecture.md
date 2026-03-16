# AI Restaurant Recommendation Service - Architecture

## System Overview
The goal of this service is to provide personalized restaurant recommendations by combining structured search (using the Zomato dataset) with the generative capabilities of a Large Language Model (LLM).

## Dataset
**Source Context**: Hugging Face - `ManikaSaini/zomato-restaurant-recommendation`
The data contains structured information about restaurants, including location, cuisine, price, and ratings, which will act as the "knowledge base" for the LLM.

---

## Project Phases

### Phase 1: Data Acquisition & Preprocessing
**Objective**: Fetch, clean, and format the Zomato dataset for efficient querying.
- **Data Ingestion**: Download the dataset from Hugging Face programmatically (e.g., using the `datasets` library or Pandas).
- **Data Cleaning**: Handle missing values, normalize text columns (e.g., standardizing cuisine types and area names), and convert price and rating strings to appropriate numeric types for filtering.
- **Data Storage**: Load the cleaned dataset into an efficient storage format. This could be an in-memory Pandas DataFrame, a lightweight SQL database (SQLite), or a Vector Database (like ChromaDB/FAISS) if semantic similarity search is desired alongside exact metric filtering.

### Phase 2: Core Recommendation Engine (Retrieval)
**Objective**: Filter data based on hard constraints from user input to prepare context for the LLM.
- **Query Processing**: Parse the user preferences:
  - `Place`: String match / Geo-search.
  - `Cuisine`: Substring / semantic match.
  - `Price`: Range filtering.
  - `Rating`: Greater-than-or-equal-to filtering.
- **Retrieval Mechanism**: Execute the query against the cleaned dataset to retrieve the top $N$ matching restaurants. 

### Phase 3: LLM Integration (Augmented Generation)
**Objective**: Generate natural, compelling, and readable recommendations.
- **Context Construction**: Format the retrieved top $N$ restaurant records into a structured, concise text string.
- **Prompt Engineering**: Design a system prompt that incorporates both the **User Preferences** and the **Retrieved Context**. The prompt will instruct the LLM to write a friendly response, detailing the options and emphasizing *why* they fit the user's specific criteria.
- **LLM Call**: Make API calls to **Groq LLM** to ensure fast, high-performance recommendation generation.

### Phase 4: API & Service Layer
**Objective**: Expose the recommendation engine as a reliable, scalable web service.
- **Framework**: Use FastAPI to create a fast, asynchronous REST API.
- **Endpoints**:
  - `POST /api/recommend`: Accepts a JSON payload with user preferences and returns the LLM-generated recommendation text.
- **Robustness**: Implement error handling, LLM timeout management, and fallback responses for cases where 0 restaurants match the given criteria.

### Phase 5: User Interface (UI) Page
**Objective**: Build a dedicated UI page to provide a simple, intuitive interface for users to enter preferences and view the final results.
- **Framework**: Streamlit or Gradio for rapid AI prototyping (or React/Vue to map the API to a full-stack web page).
- **Features**: 
  - Form inputs: Dropdowns for location/cuisine, sliders/buttons for price and minimum rating.
  - Display Area: A markdown-supported text box to render the Groq LLM's generated recommendations clearly on the UI page.

---

## Architecture Flow Diagram

```text
[ User Interface ]
        |
        | 1. Submits Preferences (Place, Price, Rating, Cuisine)
        v
[ API Layer (FastAPI) ]
        |
        | 2. Forwards criteria
        v
[ Retrieval Engine ] <========= [ Data Layer ]
        |                       (Cleaned Zomato Dataset)
        | 3. Fetches Top N Matches
        v
[ Prompt Builder ]
        |
        | 4. Combines User Prefs + Top N Matches into a Prompt
        v
[ Groq LLM ]
        |
        | 5. Generates human-readable recommendation
        v
[ API Layer ]
        |
        | 6. Returns final text
        v
[ User Interface ]
```
