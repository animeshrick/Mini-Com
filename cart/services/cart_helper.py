import uuid
from django.core.exceptions import ValidationError

class CartHelper:
    @staticmethod
    def validate_uuid(value: str) -> bool:
        try:
            uuid.UUID(str(value))
            return True
        except (ValueError, TypeError):
            return False
