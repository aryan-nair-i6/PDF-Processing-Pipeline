# PDF Processing Pipeline

An asynchronous pipeline designed to discover, extract, summarize, and store PDF content into a vector database for downstream RAG (Retrieval-Augmented Generation) applications.

## Overview

This project implements a multi-stage asynchronous processing pipeline using Python's `asyncio`. It manages the lifecycle of document processing from initial discovery in a local folder to persistence in a ChromaDB vector store.

### Pipeline Stages:
1.  **Discovery:** Scans a designated folder for new PDF files.
2.  **Extraction:** Extracts text content from the discovered PDFs.
3.  **Summarization:** Utilizes OpenAI's GPT models to generate structured summaries of the extracted text.
4.  **Loading:** Chunks the summaries and embeds them into a ChromaDB vector store for efficient retrieval.

## Features

- **Asynchronous Execution:** High-performance processing using `asyncio` queues and tasks.
- **Job Tracking:** Persistent tracking of processing stages and status using SQLAlchemy.
- **Robustness:** Built-in retry logic using `tenacity` for external API calls.
- **Vector Storage:** Integrated with ChromaDB for semantic search capabilities.
- **Extensible Architecture:** Modular service-oriented design for easy modification of individual stages.

## Tech Stack

- **Language:** Python 3.13+
- **Concurrency:** `asyncio`
- **ORMs/Databases:** SQLAlchemy, SQLite (Job tracking), ChromaDB (Vector store)
- **AI/LLM Frameworks:** LangChain, OpenAI API
- Utilities: `python-dotenv`, `tenacity`, `pypdf`

## Getting Started

### Prerequisites
- Python 3.13 or higher
- An OpenAI API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd project1_code
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    *(Note: Ensure you have a requirements.txt file or install manually based on imports)*
    ```bash
    pip install langchain-openai langchain-community langchain-text-splitters sqlalchemy aiosqlite chromadb python-dotenv tenacity pypdf
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```env
    OPENAI_KEY=your_openai_api_key_here
    ```

### Usage

Run the main pipeline:
```bash
python main.py
```

The pipeline will start monitoring the `filefolder` directory (by default) and process any PDF files found. Logs will be written to `app.log`.

## Project Structure

- `main.py`: Entry point for the asynchronous pipeline.
- `AsyncServices/`: Contains individual service modules for each pipeline stage.
- `Database/`: Database models and services for job tracking.
- `PromptsModels/`: LLM prompt templates and structured output models.
- `filefolder/`: Source directory for PDF documents.
- `vectorstore/`: Persistent storage for ChromaDB (git-ignored).
