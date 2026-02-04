# Aryma Labs RAG Chatbot
## Overview

This project implements a Retrieval Augmented Generation (RAG) chatbot that answers user questions using content from the official Aryma Labs website (https://www.arymalabs.com).
The system crawls and indexes website content, detects changes over time, and uses a RAG pipeline to generate grounded answers. It also maintains short term conversational memory within a user session and provides a simple Streamlit chat interface for interaction.

## Architecture Overview

### Data ingestion and indexing
- Crawls pages from arymalabs.com
- Extracts and cleans text content
- Chunks content into manageable pieces
- Generates embeddings
- Stores vectors in a FAISS index
- Tracks page content changes using hashing

### RAG pipeline
- Uses a retriever to fetch relevant chunks from FAISS
- Uses a LLM to answer queries using retrieved context
- Implemented using LangGraph for clear state management
- Maintains conversation context in a state object

### UI
- Built using Streamlit
- Chat style interface
- Displays assistant responses and source links
- Maintains session memory using Streamlit session state

## Set up and run instructions
### 1. Clone the repository

```
git clone <your-repo-url>
cd aryma-rag-chatbot
```

### 2. Create Virtual Environment

```
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4.Set Environment Variables

create .env file

```
OPENAI_API_KEY=your_openai_api_key
```

### 5. Run Ingestion Pipeline

```
python ingestion/run_ingestion.py
```
This step crawls the website, detects new or updated pages, and updates the embeddings and FAISS index accordingly.

### 6. Run the Chatbot UI

```
streamlit run streamlit_app.py
```

## Change detection strategy

To ensure the chatbot reflects website updates automatically:
- Each crawled page content is hashed
- Hashes are stored in a metadata file
- On subsequent crawls:
    - New pages are detected
    - Updated pages are re embedded
    - Unchanged pages are skipped
This avoids unnecessary reprocessing while ensuring the vector index remains up to date.

## Short Term Memory Implementation Details

Short term conversational memory is implemented using:
- LangGraph state for RAG context
- Streamlit session_state for session persistence

Each user session maintains:
- Chat history
- Latest user query
- Retrieved documents
- Generated answer
- Source references

Memory is scoped to a single browser session and resets automatically when the session ends.


## Demo 
![img_demo1](images/demo1.png)
*demo screenshot 1*


![img_demo2](images/demo2.png)
*demo screenshot 2*






