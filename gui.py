import os
import streamlit as st
from datetime import datetime

from inverted_index import initiate_index
from inverted_index import InvertedIndex


def date_to_datetime(date_obj):
    # Create a datetime object with time at midnight
    datetime_obj = datetime.combine(date_obj, datetime.min.time())
    return datetime_obj


def upload_and_index(uploaded_file, title, author, keywords, date, inverted_index):
    # Create 'documents' folder if it doesn't exist
    os.makedirs("documents", exist_ok=True)

    # Format the filename
    formatted_title = title.replace(" ", "%20")
    formatted_author = author.replace(" ", "%20")
    # Assuming date_time is in 'YYYY-MM-DD HH:MM:SS' format
    date_time = date_to_datetime(date)
    timestamp = date_time.timestamp()
    filename = f"{formatted_title}_{formatted_author}_{timestamp}"

    # Save the uploaded file
    file_path = os.path.join("documents", filename)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    # Add the document to the index
    inverted_index.add_document(
        uploaded_file.getvalue().decode(),
        title,
        author,
        keywords,
        date_time,
        path=file_path,
    )


def upload_page():
    st.header("Upload Document")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file")

    # Metadata fields
    title = st.text_input("Title")
    author = st.text_input("Author")
    keywords = st.text_input("Keywords")
    date = st.date_input("Date and Time")

    # Submit button
    if st.button("Upload and Index Document"):
        if uploaded_file is not None and title and author and keywords and date:
            try:
                upload_and_index(
                    uploaded_file,
                    title,
                    author,
                    keywords,
                    date,
                    inverted_index=st.session_state.inverted_index,
                )

                st.success("Document successfully uploaded and indexed.")
            except ValueError:
                st.error(
                    "Invalid date and time format. Please use YYYY-MM-DD HH:MM:SS."
                )
        else:
            st.error("Please upload a file and fill out all metadata fields.")


def search_page():
    st.header("Search Documents")
    st.text(
        """
        The documents are prioritized following these criteria (in order):
            - Highest match count
            - Most Recent
            - author, keywords, title
        """
    )

    # Search input
    query = st.text_input("Enter search query")

    # Search button
    if st.button("Search"):
        if query:
            # Perform search here
            doc_ids = st.session_state.inverted_index.search(query)

            # Placeholder for search results
            for doc_id in doc_ids:
                path = st.session_state.inverted_index.get_document_path(doc_id)
                st.write(f"{doc_id} - {path.replace('%20', ' ').replace('_', ' - ')}")
        else:
            st.error("Please enter a search query.")


def main():
    # Initialize session state
    if "inverted_index" not in st.session_state:
        st.session_state.inverted_index = (
            InvertedIndex()
        )  # Assuming InvertedIndex is your class
        initiate_index(st.session_state.inverted_index)

    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose the app mode", ["Search Documents", "Upload Document"]
    )

    if app_mode == "Upload Document":
        upload_page()
    elif app_mode == "Search Documents":
        search_page()


if __name__ == "__main__":
    main()
