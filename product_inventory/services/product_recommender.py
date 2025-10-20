import pandas as pd
from scipy.sparse import csr_matrix
import implicit


class ProductRecommender:
    """
    ALS collaborative filtering using implicit feedback (orders/quantities).
    Compatible with Python 3.13.
    """

    def __init__(self, df: pd.DataFrame):
        # Aggregate user-item data
        self.user_item = df.groupby(["user_id", "ordered_items"], as_index=False)["quantity"].sum()
        self.model = None
        self.user_mapping = {}
        self.item_mapping = {}
        self._prepare_matrix()
        self._train_model()

    def _prepare_matrix(self):
        # Ensure IDs are strings so UUIDs are preserved
        self.user_item['user_id'] = self.user_item['user_id'].astype(str)
        self.user_item['ordered_items'] = self.user_item['ordered_items'].astype(str)

        users = self.user_item["user_id"].unique()
        items = self.user_item["ordered_items"].unique()

        self.user_mapping = {u: i for i, u in enumerate(users)}
        self.item_mapping = {i: j for j, i in enumerate(items)}

        row = [self.user_mapping[u] for u in self.user_item["user_id"]]
        col = [self.item_mapping[i] for i in self.user_item["ordered_items"]]
        data = self.user_item["quantity"].astype(float)

        self.sparse_matrix = csr_matrix((data, (row, col)), shape=(len(users), len(items)))

    def _train_model(self):
        model = implicit.als.AlternatingLeastSquares(factors=50, regularization=0.1, iterations=20)
        # implicit expects item-user matrix
        model.fit(self.sparse_matrix.T)
        self.model = model

    def recommend_for_user(self, user_id: int, top_n: int = 10):
        if user_id not in self.user_mapping:
            return []

        user_idx = self.user_mapping[user_id]
        user_vector = self.sparse_matrix[user_idx]

        recs = self.model.recommend(
            user_idx, user_vector, N=top_n, filter_already_liked_items=True
        )

        reverse_item_mapping = {v: k for k, v in self.item_mapping.items()}
        recommendations = [(reverse_item_mapping[i], float(score)) for i, score in recs]

        return recommendations
