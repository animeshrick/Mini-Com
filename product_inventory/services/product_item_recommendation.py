from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from product_inventory.models import Product


def product_item_recommendation(product_id: str, top_N=5):
    vectorizer = TfidfVectorizer(stop_words="english")
    all_products = Product.objects.all()
    all_product_brands = [p.brand if p.brand else "" for p in all_products]
    tfid_matrix = vectorizer.fit_transform(all_product_brands)
    target_product = Product.objects.get(id=product_id)
    list_all_products = list(all_products)
    target_product_index = list_all_products.index(target_product)

    cosine_sim = cosine_similarity(tfid_matrix[target_product_index], tfid_matrix).flatten()
    similar_indices = cosine_sim.argsort()[-top_N-1:-1][::1]
    similar_indices = [i for i in similar_indices if i != target_product_index]
    similar_products = []
    for i in similar_indices:
        similar_products.append(list_all_products[i])
    return similar_products