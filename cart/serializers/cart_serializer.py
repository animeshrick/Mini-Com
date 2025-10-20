from typing import Optional
from django.db import transaction
from rest_framework import serializers
from _decimal import Decimal

from auth_api.models import User
from cart.export_types.request_data_types.add_update_delete import AddUpdatedDeleteCartRequestType
from cart.models import Cart, CartItem
from cart.services.cart_helper import CartHelper
from product_inventory.models import Product


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

    def validate(self, data: Optional[AddUpdatedDeleteCartRequestType] = None) -> bool:
        """
        Validate incoming request data

        Args:
            data: Request data containing user_id, action, and products

        Returns:
            bool: True if validation passes

        Raises:
            ValueError: If validation fails
        """
        # Validate user exists and is active
        try:
            user = User.objects.get(id=data.user_id, is_deleted=False, is_active=True)
        except User.DoesNotExist:
            raise ValueError("User not found or is inactive")

        # Validate action
        action = data.action.upper()
        if action not in ["A", "U", "D"]:
            raise ValueError("Action must be A (Add), U (Update), or D (Delete)")

        # Validate products
        if not data.products or len(data.products) == 0:
            raise ValueError("Products list cannot be empty")

        for item in data.products:
            # Validate product exists
            try:
                if not CartHelper().validate_uuid(str(item.product_id)):
                    raise ValueError(f"Product ID {item.product_id} is not a valid UUID")
                product = Product.objects.get(id=item.product_id, is_active=True)
            except Product.DoesNotExist:
                raise ValueError(f"Product {item.product_id} not found or is not available")

            # For Add/Update actions, validate stock and quantity
            if action in ["A", "U"]:
                if item.quantity <= 0:
                    raise ValueError(f"Quantity must be greater than zero for product {product.name}")

                # For Add: check if we have enough stock
                if action == "A":
                    try:
                        existing_cart = Cart.objects.get(user=user, is_active=True)
                        existing_item = CartItem.objects.filter(
                            cart=existing_cart,
                            product=product
                        ).first()

                        required_stock = item.quantity
                        if existing_item:
                            required_stock += existing_item.quantity

                        if product.stock < required_stock:
                            raise ValueError(
                                f"Insufficient stock for {product.name}. "
                                f"Available: {product.stock}, Required: {required_stock}"
                            )
                    except Cart.DoesNotExist:
                        if product.stock < item.quantity:
                            raise ValueError(
                                f"Insufficient stock for {product.name}. "
                                f"Available: {product.stock}, Required: {item.quantity}"
                            )

                # For Update: check if new quantity is within stock
                elif action == "U":
                    if product.stock < item.quantity:
                        raise ValueError(
                            f"Insufficient stock for {product.name}. "
                            f"Available: {product.stock}, Requested: {item.quantity}"
                        )

        return True

    @transaction.atomic  # Ensures all DB operations succeed or rollback
    def create(self, data: AddUpdatedDeleteCartRequestType) -> Optional[Cart]:
        """
        Handle Add/Update/Delete operations on cart

        Args:
            data: Request data with action and products

        Returns:
            Cart: Updated or created cart object
            None: If validation fails
        """
        # Validate the incoming data
        if not self.validate(data):
            return None

        # Get user and determine action
        user = User.objects.get(id=data.user_id)
        action = data.action.upper()

        # Check for existing active cart
        existing_cart = Cart.objects.filter(user=user, is_active=True).first()

        # ============== DELETE ACTION ==============
        if action == "D":
            cart = self._handle_delete(existing_cart, data.products)
            cart.total_cart_price = self._calculate_cart_total(cart)
            return cart

        # ============== ADD ACTION ==============
        elif action == "A":
            cart = self._handle_add(existing_cart, user, data.products)
            cart.total_cart_price = self._calculate_cart_total(cart)
            return cart

        # ============== UPDATE ACTION ==============
        elif action == "U":
            cart = self._handle_update(existing_cart, user, data.products)
            cart.total_cart_price = self._calculate_cart_total(cart)
            return cart

        return None

    def _calculate_cart_total(self, cart: Cart) -> Decimal:
        """
        Calculate total price of all items in the cart

        Args:
            cart: Cart object with cart_items loaded

        Returns:
            Decimal: Total price of all items
        """
        from decimal import Decimal

        if not cart:
            return Decimal('0.00')

        total = Decimal('0.00')

        # Access cart items using the related_name
        for cart_item in cart.cart_items.all():
            if cart_item.product and cart_item.quantity:
                # Calculate: product.price * quantity
                item_subtotal = cart_item.product.price * cart_item.quantity
                total += item_subtotal

        return total

    def _handle_delete(self, cart: Optional[Cart], products: list) -> Cart:
        """Handle DELETE action - remove items from cart"""
        if not cart:
            raise ValueError("No active cart found to delete items from")

        cart_modified = False

        for cart_item_data in products:
            try:
                product = Product.objects.get(id=cart_item_data.product_id)
                cart_item = CartItem.objects.get(cart=cart, product=product)

                # Return stock before deleting
                product.stock += cart_item.quantity
                product.save(update_fields=['stock'])

                # Delete the cart item
                cart_item.delete()
                cart_modified = True

            except (Product.DoesNotExist, CartItem.DoesNotExist):
                # Item not in cart or product not found, skip
                continue

        # Update cart's updated_at if modified
        if cart_modified:
            cart.save(update_fields=['updated_at'])

        cart.refresh_from_db()
        return cart

    def _handle_add(self, cart: Optional[Cart], user: User, products: list) -> Cart:
        """Handle ADD action - add items to cart or create new cart"""
        if cart:
            # Add to existing cart
            cart_modified = False

            for cart_item_data in products:
                product = Product.objects.select_for_update().get(id=cart_item_data.product_id)

                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': cart_item_data.quantity}
                )

                if created:
                    # New item created
                    product.stock -= cart_item_data.quantity
                    product.save(update_fields=['stock'])
                    cart_modified = True
                else:
                    # Item exists - ADD to existing quantity
                    cart_item.quantity += cart_item_data.quantity
                    cart_item.save(update_fields=['quantity'])

                    product.stock -= cart_item_data.quantity
                    product.save(update_fields=['stock'])
                    cart_modified = True

            # Update cart's updated_at if modified
            if cart_modified:
                cart.save(update_fields=['updated_at'])

            cart.refresh_from_db()
            return cart

        else:
            # Create new cart
            cart = Cart.objects.create(user=user, is_active=True)

            # Prepare cart items for bulk creation
            cart_items = []
            products_to_update = []

            for cart_item_data in products:
                product = Product.objects.select_for_update().get(id=cart_item_data.product_id)

                cart_items.append(CartItem(
                    cart=cart,
                    product=product,
                    quantity=cart_item_data.quantity
                ))

                # Update stock
                product.stock -= cart_item_data.quantity
                products_to_update.append(product)

            # Bulk operations
            CartItem.objects.bulk_create(cart_items)
            Product.objects.bulk_update(products_to_update, ['stock'])

            cart.refresh_from_db()
            return cart

    def _handle_update(self, cart: Optional[Cart], user: User, products: list) -> Cart:
        """Handle UPDATE action - replace item quantities"""
        if not cart:
            raise ValueError("No active cart found to update")

        cart_modified = False

        for cart_item_data in products:
            product = Product.objects.select_for_update().get(id=cart_item_data.product_id)

            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)

                # Check if quantity is different
                if cart_item.quantity == cart_item_data.quantity:
                    # Same quantity - do nothing
                    continue

                # Different quantity - REPLACE with new quantity
                old_quantity = cart_item.quantity
                quantity_difference = cart_item_data.quantity - old_quantity

                cart_item.quantity = cart_item_data.quantity
                cart_item.save(update_fields=['quantity'])

                # Adjust stock based on difference
                product.stock -= quantity_difference
                product.save(update_fields=['stock'])

                cart_modified = True

            except CartItem.DoesNotExist:
                # New item - add to cart
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=cart_item_data.quantity
                )

                product.stock -= cart_item_data.quantity
                product.save(update_fields=['stock'])

                cart_modified = True

        # Update cart's updated_at if modified
        if cart_modified:
            cart.save(update_fields=['updated_at'])

        cart.refresh_from_db()
        return cart