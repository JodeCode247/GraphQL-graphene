
import os
import django
import json


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_graghql.settings')
django.setup()

from customer.models import Questions, Options, Answer


quiz_data = [
  {
    "id": 1,
    "question": "What is the capital of France?",
    "options": {
      "a": "London",
      "b": "Berlin",
      "c": "Paris",
      "d": "Rome"
    },
    "answer": "c"
  },
  {
    "id": 2,
    "question": "Which planet is known as the Red Planet?",
    "options": {
      "a": "Jupiter",
      "b": "Mars",
      "c": "Saturn",
      "d": "Venus"
    },
    "answer": "b"
  },
  {
    "id": 3,
    "question": "What is the largest ocean on Earth?",
    "options": {
      "a": "Atlantic Ocean",
      "b": "Indian Ocean",
      "c": "Arctic Ocean",
      "d": "Pacific Ocean"
    },
    "answer": "d"
  },
  {
    "id": 4,
    "question": "What is the boiling point of water in Celsius?",
    "options": {
      "a": "0°C",
      "b": "50°C",
      "c": "100°C",
      "d": "212°C"
    },
    "answer": "c"
  },
  {
    "id": 5,
    "question": "Who wrote 'Romeo and Juliet'?",
    "options": {
      "a": "Charles Dickens",
      "b": "William Shakespeare",
      "c": "Jane Austen",
      "d": "Mark Twain"
    },
    "answer": "b"
  },
  {
    "id": 6,
    "question": "What is the main ingredient in guacamole?",
    "options": {
      "a": "Tomato",
      "b": "Onion",
      "c": "Avocado",
      "d": "Lime"
    },
    "answer": "c"
  },
  {
    "id": 7,
    "question": "Which country is home to the kangaroo?",
    "options": {
      "a": "New Zealand",
      "b": "South Africa",
      "c": "Australia",
      "d": "Brazil"
    },
    "answer": "c"
  },
  {
    "id": 8,
    "question": "What is the chemical symbol for gold?",
    "options": {
      "a": "Au",
      "b": "Ag",
      "c": "Fe",
      "d": "Pb"
    },
    "answer": "a"
  },
  {
    "id": 9,
    "question": "How many continents are there in the world?",
    "options": {
      "a": "5",
      "b": "6",
      "c": "7",
      "d": "8"
    },
    "answer": "c"
  },
  {
    "id": 10,
    "question": "What is the currency of Japan?",
    "options": {
      "a": "Yuan",
      "b": "Won",
      "c": "Yen",
      "d": "Baht"
    },
    "answer": "c"
  }
]

def populate_database():
    
    print("Clearing old data...")
    Questions.objects.all().delete()
    print("Old data cleared.")
    print("Starting to populate database with new questions...")

    for item in quiz_data:
        try:
            # 1. Create the Questions instance
            question = Questions.objects.create(text=item['question'])
            print(f"Created question: '{question.text}'")

            # 2. Create the Options for the question
            for option_alphabet, option_text in item['options'].items():
                Options.objects.create(
                    question=question,
                    option_alphabet=option_alphabet,
                    option_text=option_text
                )
            print(f"  -> Created options for question {question.id}")

            # 3. Create the Answer for the question
            Answer.objects.create(
                question=question,
                answer_alphabet=item['answer']
            )
            print(f"  -> Set answer for question {question.id}")
            print("-" * 20)

        except Exception as e:
            print(f"An error occurred while processing question {item['id']}: {e}")

    print("\nDatabase population complete!")

# Run the function
if __name__ == '__main__':
    populate_database()
