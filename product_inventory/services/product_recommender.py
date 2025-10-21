import pandas as pd
from scipy.sparse import csr_matrix
import implicit
import matplotlib.pyplot as plt
import seaborn as sns


class ProductRecommender:
    """
    ALS collaborative filtering using implicit feedback (orders/quantities).
    Compatible with Python 3.13.
    """

    def __init__(self, df: pd.DataFrame):

        v = df.groupby(["user_id", "ordered_items"], as_index=False)["quantity"].sum()

        # Aggregate user-item data
        self.user_item = v
        self.model = None
        self.user_mapping = {}
        self.item_mapping = {}
        self._prepare_matrix()
        self._train_model()

    def _prepare_matrix(self):
        self.user_item['user_id'] = self.user_item['user_id'].astype(str)
        self.user_item['ordered_items'] = self.user_item['ordered_items'].astype(str)

        users = sorted(self.user_item["user_id"].unique())
        items = sorted(self.user_item["ordered_items"].unique())

        self.user_mapping = {u: idx for idx, u in enumerate(users)}
        self.item_mapping = {i: idx for idx, i in enumerate(items)}

        row = [self.user_mapping[u] for u in self.user_item["user_id"]]
        col = [self.item_mapping[i] for i in self.user_item["ordered_items"]]
        data = self.user_item["quantity"].astype(float)

        self.sparse_matrix = csr_matrix((data, (row, col)), shape=(len(users), len(items)))

    def _train_model(self):
        model = implicit.als.AlternatingLeastSquares(factors=50, regularization=0.1, iterations=20)
        # implicit expects item-user matrix
        model.fit(self.sparse_matrix)
        self.model = model

    def recommend_for_user(self, user_id: str, top_n: int = 10):
        if user_id not in self.user_mapping:
            return []

        # Edge case: If there's only one unique item in the entire dataset,
        # we cannot recommend anything new.
        if self.sparse_matrix.shape[1] <= 1:
            return []

        num_users, num_items = self.sparse_matrix.shape
        if num_items <= 1:
            print("⚠️ Not enough users or items for collaborative filtering.")
            return []

        user_idx = self.user_mapping[user_id]
        print("User index:", user_idx)

        # user_vector = self.sparse_matrix[user_idx]
        #
        # recs = self.model.recommend(
        #     user_idx, user_vector, N=top_n, filter_already_liked_items=True
        # )

        print("Matrix shape:", self.sparse_matrix.shape)
        print("Onion shape:", self.item_mapping.items())

        csr_grid = self.sparse_matrix
        print("Onion csr_grid:", csr_grid)

        if user_idx >= num_users:
            print(f"⚠️ user_idx {user_idx} out of range for matrix with {num_users} rows.")
            return []

        recs = self.model.recommend(
            user_idx,
            csr_grid,
            N=top_n,
            filter_already_liked_items=True
        )
        print("Onion recs:", recs)

        # ✅ Handle internal error
        # if not isinstance(recs, list):
        #     print("⚠️ Recommend returned error:", recs)
        #     return []

        reverse_item_mapping = {v: k for k, v in self.item_mapping.items()}

        recommendations = []
        for item_idx, score in zip(recs[0], recs[1]):
            product_id = reverse_item_mapping[item_idx]
            recommendations.append((product_id, float(score)))

        # recommendations = [(reverse_item_mapping[i], float(score)) for i, score in recs]

        return recommendations

    def visualize_matrix(self, max_users=50, max_items=100):
        """
        Visualizes the user-item interaction matrix as a heatmap.

        To prevent memory errors, this will only plot a slice of the matrix
        if it is larger than the specified max dimensions.
        """
        if self.sparse_matrix is None:
            print("Matrix has not been prepared yet.")
            return

        num_users, num_items = self.sparse_matrix.shape
        
        # Calculate sparsity
        total_elements = num_users * num_items
        if total_elements == 0:
            sparsity = 1.0
        else:
            sparsity = 1 - (self.sparse_matrix.nnz / total_elements)

        print(f"User-Item Matrix Shape: {num_users} users x {num_items} items")
        print(f"Sparsity: {sparsity:.4%}")

        # Decide whether to plot the full matrix or a slice
        plot_users = min(num_users, max_users)
        plot_items = min(num_items, max_items)
        
        # Convert the slice to a dense array for plotting
        matrix_slice = self.sparse_matrix[:plot_users, :plot_items].toarray()

        plt.figure(figsize=(15, 15 * (plot_users / plot_items)))
        sns.heatmap(matrix_slice, cmap="viridis", cbar_kws={'label': 'Interaction Strength (Quantity)'})
        plt.title(f"User-Item Interaction Matrix (Slice: {plot_users}x{plot_items})")
        plt.xlabel("Products (Mapped IDs)")
        plt.ylabel("Users (Mapped IDs)")
        plt.show()
