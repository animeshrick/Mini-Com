from django.db import models


# 1= place, 2=dispatched, 3= delivered, 4 =cancelled, 5 = returned
class OrderStatus(models.TextChoices):
    PLACED = 'placed', 'Placed'
    DISPATCHED = 'dispatched', 'Dispatched'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'
    RETURNED = 'returned', 'Returned'