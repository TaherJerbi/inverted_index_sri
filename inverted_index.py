from collections import Counter, defaultdict
from datetime import datetime
import os
import re
import pickle


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)
        self.documents = {}
        self.metadata = {}
        self.doc_id = 0
        self.stop_words = set(
            [
                "a",
                "an",
                "the",
                "is",
                "are",
                "was",
                "were",
                "this",
                "that",
                "of",
                "for",
                "on",
                "in",
            ]
        )

    def add_document(
        self,
        document: str,
        title: str,
        author: str,
        keywords: str,
        date_time: datetime,
        path="",
    ):
        # Process the document
        words = re.findall(r"\w+", document.lower())
        filtered_words = [word for word in words if word not in self.stop_words]

        # Add the document and its metadata
        self.documents[self.doc_id] = document
        self.metadata[self.doc_id] = {
            "title": title,
            "author": author.lower(),
            "keywords": keywords.lower(),
            "date_time": date_time,
            "path": path,
        }

        # Update the index for document content
        for word in filtered_words:
            self.index[word].add(self.doc_id)

        # Also index the author and keywords
        for word in re.findall(r"\w+", author.lower()):
            self.index[word].add(self.doc_id)
        for word in re.findall(r"\w+", keywords.lower()):
            self.index[word].add(self.doc_id)
        for word in re.findall(r"\w+", title.lower()):
            self.index[word].add(self.doc_id)

        self.doc_id += 1

    def search(self, query):
        query_words = set(re.findall(r"\w+", query.lower()))
        filtered_query_words = [
            word for word in query_words if word not in self.stop_words
        ]

        # Find document IDs with match count
        match_count = Counter()
        for word in filtered_query_words:
            if word in self.index:
                for doc_id in self.index[word]:
                    match_count[doc_id] += 1

        # Prioritize search results
        sorted_results = sorted(
            match_count.keys(),
            key=lambda doc_id: (
                # More matches are more relevant
                match_count[doc_id],
                # Most recent first
                -self.metadata[doc_id]["date_time"].timestamp(),
                # Prioritize if author or keywords match the query
                any(
                    word in self.metadata[doc_id]["author"]
                    for word in filtered_query_words
                ),
                any(
                    word in self.metadata[doc_id]["keywords"]
                    for word in filtered_query_words
                ),
                any(
                    word in self.metadata[doc_id]["title"]
                    for word in filtered_query_words
                ),
            ),
            reverse=True,
        )

        return sorted_results

    def get_document_path(self, doc_id):
        return self.metadata[doc_id]["path"]

    def save_to_file(self, file_path):
        # Serialize the index and associated data to a file
        with open(file_path, "wb") as file:
            pickle.dump((self.index, self.documents, self.metadata, self.doc_id), file)

    def load_from_file(self, file_path):
        # Deserialize the index and associated data from a file
        with open(file_path, "rb") as file:
            self.index, self.documents, self.metadata, self.doc_id = pickle.load(file)


def initiate_index(inverted_index: InvertedIndex, documents_folder="documents"):
    for filename in os.listdir(documents_folder):
        # Ensure the file is a regular file (and not a directory, etc.)
        if os.path.isfile(os.path.join(documents_folder, filename)):
            # Extract title, author, and timestamp from the filename
            title, author, timestamp = filename.rsplit("_", 2)
            title = title.replace("%20", " ")
            author = author.replace("%20", " ")
            date_time = datetime.fromtimestamp(float(timestamp))
            # Read the file content
            with open(os.path.join(documents_folder, filename), "r") as file:
                document_content = file.read()

            # Add the document to the index
            inverted_index.add_document(
                document_content,
                title,
                author,
                "",
                date_time,
                path=documents_folder + "/" + filename,
            )
