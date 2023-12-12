import os
import datetime
import time


def create_test_files(folder="documents"):
    # Create the folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    # Predefined data for test files
    data = [
        (
            "Space Exploration",
            "Jane Smith",
            "Exploring the vast universe has always been a human fascination. The mysteries of space continue to intrigue scientists and explorers alike.",
        ),
        (
            "Ocean Depths",
            "John Doe",
            "The ocean's depths hide some of the world's most astonishing creatures. Exploring these depths has revealed surprising secrets.",
        ),
        (
            "Mountain Climbing",
            "Alice Johnson",
            "Mountain climbing is not just a sport, but a journey towards self-discovery. Each peak offers a new challenge and a new adventure.",
        ),
        (
            "Desert Survival",
            "Mohamed Ali",
            "Surviving in the desert requires knowledge and resilience. The harsh environment tests the limits of human endurance.",
        ),
        (
            "Artificial Intelligence",
            "Emma Clark",
            "Artificial Intelligence is revolutionizing our world, from automating mundane tasks to solving complex problems.",
        ),
        (
            "Quantum Computing",
            "Liu Wei",
            "Quantum computing represents a significant leap forward in computational capability, with potential to solve previously intractable problems.",
        ),
        (
            "Renewable Energy",
            "Ahmed Khan",
            "The future of our planet hinges on renewable energy. Harnessing the power of nature could be the key to sustainable living.",
        ),
        (
            "Ancient Civilizations",
            "Sarah Johnson",
            "Studying ancient civilizations reveals the roots of human culture and knowledge. These civilizations laid the foundations of the modern world.",
        ),
        (
            "Modern Architecture",
            "Carlos Garcia",
            "Modern architecture combines aesthetics with functionality, using innovative designs and materials to create unique spaces.",
        ),
        (
            "Deep Sea Mysteries",
            "Anna Ivanova",
            "The deep sea is one of the least explored areas on Earth. Its mysteries and inhabitants are a subject of ongoing research.",
        ),
    ]

    for title, author, content in data:
        # Format title and author for filename
        formatted_title = title.replace(" ", "%20")
        formatted_author = author.replace(" ", "%20")

        # Generate a timestamp
        timestamp = datetime.datetime.now().timestamp()

        # Create the filename
        filename = f"{formatted_title}_{formatted_author}_{timestamp}"

        # Write the file
        with open(os.path.join(folder, filename), "w") as file:
            file.write(content + "\n")

        # To ensure unique timestamps
        time.sleep(1)


# Generate test files
create_test_files()
