# Document Indexing and Search Application

## Introduction

This project is a document indexing and search application designed to efficiently manage and retrieve text-based documents. The application offers a user-friendly interface built with Streamlit, allowing users to upload documents with specific metadata, index them for quick retrieval, and perform searches based on various criteria.

## Installation

The project primarily relies on Streamlit as its external library. To set up the project, follow these steps:

1. Ensure you have Python installed on your system.
2. Install Streamlit using pip:

```bash
pip install streamlit
```

## Usage

To run the application:

1. Navigate to the project directory.
2. Run the GUI with the command:

```bash
streamlit run gui.py
```

3. Use the sidebar to switch between the upload and search pages.
   - **Search Page**: Use this page to query for documents. Enter your search criteria and the application will display relevant documents based on the index.
   - **Upload Page**: Use this page to upload new documents. Fill in the necessary metadata and the document will be indexed for future searches.

## Features

### Inverted Index

At the core of this application is the InvertedIndex class ([inverted_index.py](inverted_index.py)), which is responsible for creating and managing an inverted index. This class indexes text-based documents, allowing for quick and effective searching. It supports adding new documents to the index and searching through the documents using keywords, authors' names, and other metadata.

The class is designed with features like automatic and manual indexation, prioritizing search results based on date, authorship, keyword relevance, and frequency of terms.

### Searching the Index

The documents are prioritized based on the following criteria (in order):

- Highest match count.
- Most recent.
- Author, keywords, Title.
