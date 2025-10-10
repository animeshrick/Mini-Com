from cart.export_types.request_data_types.add_update_delete import AddUpdatedDeleteCartRequestType
from cart.models import Cart


class CartServices:
    @staticmethod
    def add_update_delete_cart_service(request_data: AddUpdatedDeleteCartRequestType) -> Cart:
        print(f"request_data: {request_data.products} {request_data.user_id} {request_data.action}")
        return Cart()
