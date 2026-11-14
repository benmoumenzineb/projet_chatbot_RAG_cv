# CV Assistant – RAG Chatbot

## Project Overview

This project implements an AI-powered chatbot based on Retrieval-Augmented Generation (RAG), designed to interact with and retrieve information from indexed CV documents.

The chatbot allows users to ask questions about CV content and obtain relevant answers using a Large Language Model (LLM) combined with document retrieval.

## Key Features

- CV document processing and indexing.
- Semantic retrieval of relevant information.
- Context-aware question answering.
- RAG pipeline for connecting retrieved documents with an LLM.
- Interactive chatbot interface.

## Architecture

The project is organized into two main components:

- **pipeline.py:** Handles the RAG pipeline and document processing.
- **app.py:** Implements the chatbot application and user interface.

## Technologies Used

- Python
- LangChain
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Streamlit

## Project Structure

```text
CV-RAG-Chatbot/
│
├── app.py
├── pipeline.py
└── README.md
```

## How to Run

1. Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

2. Navigate to the project directory:

```bash
cd CV-RAG-Chatbot
```

3. Install the required dependencies according to the project imports.

4. Run the Streamlit application:

```bash
streamlit run app.py
```

## Project Objective

The objective is to explore the practical application of Generative AI and RAG architectures to build an intelligent document-based question-answering system.

## Author

**Zineb Ben Moumen**

AI & Data Science Engineering Student
