# from symspellpy import SymSpell, Verbosity
# from rapidfuzz import process
# import re
#
#
# class SpellCorrector:
#     def __init__(self, max_edit_distance=3, prefix_length=7):
#         self.sym_spell = SymSpell(max_dictionary_edit_distance=max_edit_distance, prefix_length=prefix_length)
#         self.dictionary_entries = set()  # keep for fuzzy fallback
#
#     def build_spell_dictionary(self, product_list):
#         """
#         Build dictionary from product list.
#         Adds product name, brand, category, and description.
#         """
#         for product in product_list:
#             name = (getattr(product, "name", "") or "").lower().strip()
#             brand = (getattr(product, "brand", "") or "").lower().strip()
#             category = (
#                 (getattr(product.category, "name", "") if getattr(product, "category", None) else "")
#                 .lower()
#                 .strip()
#             )
#             description = (getattr(product, "description", "") or "").lower().strip()
#
#             for text in [name, brand, category, description]:
#                 if text:
#                     # Split into words and add individually
#                     for token in re.split(r"\s+", text):
#                         if token:
#                             self.dictionary_entries.add(token)
#                             self.sym_spell.create_dictionary_entry(token, 1)
#
#                     # Then add the full phrase too
#                     self.dictionary_entries.add(text)
#                     self.sym_spell.create_dictionary_entry(text, 1)
#
#     def correct_spell(self, user_query: str) -> str:
#         """
#         Returns corrected query string.
#         1. Try SymSpell
#         2. If no correction found, fallback to fuzzy match (RapidFuzz)
#         """
#         if not user_query or not user_query.strip():
#             return user_query
#
#         query = user_query.lower().strip()
#         dynamic_max = 1 if len(query) <= 4 else 2 if len(query) <= 7 else 3
#
#         # Step 1: Try SymSpell
#         suggestions = self.sym_spell.lookup(query, Verbosity.CLOSEST, max_edit_distance=dynamic_max)
#         if suggestions:
#             top = suggestions[0].term
#             if len(top.split()) > 2 and len(user_query.split()) == 1:
#                 # user typed a single word, avoid mapping to a multi-word product
#                 # find a shorter suggestion instead
#                 shorter = [s for s in suggestions if len(s.term.split()) == 1]
#                 if shorter:
#                     return shorter[0].term
#             return top
#
#         # Step 2: Fuzzy fallback (RapidFuzz)
#         if self.dictionary_entries:
#             best_match = process.extractOne(query, self.dictionary_entries, score_cutoff=70)
#             if best_match:
#                 return best_match[0]
#
#         # Step 3: No correction possible
#         return user_query


from symspellpy import SymSpell

from product_inventory.models import Product


class SpellCorrector:
    def __init__(self):
        self.sym_spell = SymSpell(max_dictionary_edit_distance=3, prefix_length=7)
        self._load_dictionary()

    def _load_dictionary(self):
        get_all_products = Product.objects.all()

        for product in get_all_products:
            name = product.name.lower()
            self.sym_spell.create_dictionary_entry(name, 1)

            # Index sub-tokens to help partial matches
            for token in name.split():
                self.sym_spell.create_dictionary_entry(token, 1)

            if product.brand:
                self.sym_spell.create_dictionary_entry(product.brand.lower(), 1)
            if product.category:
                self.sym_spell.create_dictionary_entry(product.category.name.lower(), 1)

    def correct_spell(self, user_query: str) -> str:
        query = user_query.lower().strip()

        # Already valid word or phrase?
        if query in self.sym_spell.words:
            return query

        # Dynamic edit distance
        max_dist = self._get_max_distance(query)

        # Compound lookup for multi-word correction
        suggestions = self.sym_spell.lookup_compound(query, max_edit_distance=max_dist)

        if not suggestions:
            return query

        top = suggestions[0]
        if not self._is_reasonable_correction(query, top.term, top.distance):
            return query

        return top.term

    def _get_max_distance(self, query):
        if len(query) <= 4:
            return 1
        elif len(query) <= 7:
            return 2
        return 3

    def _is_reasonable_correction(self, original, corrected, distance):
        if distance > 3:
            return False
        if len(corrected) < len(original) * 0.5:
            return False
        overlap = len(set(original) & set(corrected)) / len(set(original))
        return overlap >= 0.5
