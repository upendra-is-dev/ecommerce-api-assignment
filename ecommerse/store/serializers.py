from rest_framework import serializers
from .constraints.globals import Users, Items, CartData, DiscountCodes

class AddToCartSerializer(serializers.Serializer):
    """
    Serializer for adding an item to a user's cart.

    Fields:
        user_id (str): The ID of the user adding the item.
        item_id (str): The ID of the item to be added.
        quantity (int): The number of units to add (minimum value is 1).
    """
    
    user_id = serializers.CharField()
    item_id = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)
    
    def validate_user_id(self, value):
        """
        Validate that the user ID exists in the global Users list.
        Args: value (str): The user ID to validate.
        Returns: str: The validated user ID.
        Raises: serializers.ValidationError: If the user ID is not found.
        """
        
        if value not in Users:
            raise serializers.ValidationError("Invalid user.")
        return value

    def validate_item_id(self, value):
        """
        Validate that the item ID exists in the global Items list.
        Args: value (str): The item ID to validate.
        Returns: str: The validated item ID.
        Raises: serializers.ValidationError: If the item ID is not found.
        """
        if value not in Items:
            raise serializers.ValidationError("Invalid item.")
        return value


class CheckoutSerializer(serializers.Serializer):
    """
    Serializer for checking out items in a user's cart.
    Fields:
        user_id (str): The ID of the user attempting to check out.
        discount_code (str, optional): An optional discount code to apply.
    """
    
    user_id = serializers.CharField()
    discount_code = serializers.CharField(required=False)

    def validate(self, data):
        """
        Validate the checkout request.

        Ensures:
        - The user has items in their cart.
        - If a discount code is provided, it must be valid and unused.

        Args:
            data (dict): The input data to validate.

        Returns: dict: The validated data.
        Raises:serializers.ValidationError: If the cart is empty or discount code is invalid/used.
        """
        
        user_id = data.get('user_id')
        discount_code = data.get('discount_code')
        if user_id not in CartData or not CartData[user_id]:
            raise serializers.ValidationError("Cart is empty.")
        else:
            if not DiscountCodes and discount_code:
                raise serializers.ValidationError("Invalid or already used discount code. Remove discount code from body.")
            else:    
                for code in DiscountCodes:
                    if code["code"] != discount_code or (code["code"] == discount_code and code["used"]):
                        raise serializers.ValidationError("Invalid or already used discount code.")    
        return data

