from collections import Counter, defaultdict
from datetime import datetime
import re


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

    def add_document(self, document, author, keywords, date_time):
        # Process the document
        words = re.findall(r"\w+", document.lower())
        filtered_words = [word for word in words if word not in self.stop_words]

        # Add the document and its metadata
        self.documents[self.doc_id] = document
        self.metadata[self.doc_id] = {
            "author": author.lower(),
            "keywords": keywords.lower(),
            "date_time": datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S"),
        }

        # Update the index for document content
        for word in filtered_words:
            self.index[word].add(self.doc_id)

        # Also index the author and keywords
        for word in re.findall(r"\w+", author.lower()):
            self.index[word].add(self.doc_id)
        for word in re.findall(r"\w+", keywords.lower()):
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
                # More matches are more relevant
                match_count[doc_id],
            ),
            reverse=True,
        )

        return sorted_results


# Example usage
inverted_index = InvertedIndex()
# Adding a few more documents with diverse authors, keywords, and content for testing
inverted_index.add_document(
    "Analysis of financial markets in 2023.",
    "Emma Clark",
    "finance, markets, analysis",
    "2023-04-01 09:30:00",
)
inverted_index.add_document(
    "Advancements in AI and machine learning.",
    "Mohamed Ali",
    "AI, machine learning, technology",
    "2023-05-15 15:45:00",
)
inverted_index.add_document(
    "The history of ancient civilizations.",
    "Liu Wei",
    "history, ancient civilizations, archaeology",
    "2023-03-20 11:00:00",
)
inverted_index.add_document(
    "Modern web development trends.",
    "Sarah Johnson",
    "web development, technology, trends",
    "2023-06-01 08:15:00",
)
inverted_index.add_document(
    "Exploring quantum computing.",
    "Ahmed Khan",
    "quantum computing, technology",
    "2023-07-05 10:00:00",
)

# Test queries with different scenarios
test_queries = [
    "machine learning",  # Query related to a specific topic
    "Emma Clark",  # Query for an author's name
    "finance markets",  # Query containing multiple keywords
    "ancient civilizations",  # Query for a specific subject
    "technology",  # A broad topic query
    "Sarah Johnson trends",  # Query combining author's name and topic
]

# Perform searches for each test query
test_results = {query: inverted_index.search(query) for query in test_queries}
test_results
