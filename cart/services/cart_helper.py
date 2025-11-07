import uuid
import re
from transformers import pipeline

from helper.spell_correcter import SpellCorrector


class CartHelper:
    @staticmethod
    def validate_uuid(value: str) -> bool:
        try:
            uuid.UUID(str(value))
            return True
        except (ValueError, TypeError):
            return False

    extractor = pipeline("text2text-generation", model="google/flan-t5-small")

    @staticmethod
    def extract_products(text: str)-> dict:
        # Map number words to digits
        word_to_num = {
            "one": 1, "two": 2, "three": 3, "four": 4,
            "five": 5, "six": 6, "seven": 7, "eight": 8,
            "nine": 9, "ten": 10
        }

        # Normalize text
        text = text.lower()

        # Step 1: Remove special characters (keep only letters, numbers, and spaces)
        clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        spell_correct = SpellCorrector().correct_spell(user_query=clean_text)
        print(spell_correct)

        # Find patterns like "two calpol" or "1 horlicks"
        pattern = r'(\b(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)\b)\s+([a-zA-Z]+)'
        matches = re.findall(pattern, clean_text)

        result = []
        for qty_word, product in matches:
            qty = int(qty_word) if qty_word.isdigit() else word_to_num.get(qty_word, 1)
            result.append({"product_query": product.capitalize(), "quantity": qty})

        print(result)
        return {}

