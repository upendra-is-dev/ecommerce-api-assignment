# ecommerce/views/cart_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddToCartSerializer, CheckoutSerializer
from .utils import generate_discount_code
from .constraints.globals import (
    CartData, Orders, DiscountCodes, OrderCount,
    NTH_ORDER, DISCOUNT_PERCENTAGE, Items
)

class AddToCartView(APIView):
    """
    API view to handle adding an item to a user's shopping cart.

    POST:
        Accepts user_id, item_id, and quantity.
        - Validates user and item.
        - Adds the item to the user's cart.
        - If the item is already in the cart, it updates the quantity.
        - Returns a success message with the updated cart data.
    """
    def post(self, request):
        """
        Handle POST request to add an item to the cart.
        Args: request (HttpRequest): The incoming request containing user_id, item_id, and quantity.
        Returns: Response: A success response with updated cart details if valid,
                otherwise returns validation errors.
        """
        
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            item_id = serializer.validated_data['item_id']
            quantity = serializer.validated_data['quantity']

            item_price = Items[item_id]['price']
            user_cart = CartData.setdefault(user_id, [])

            for item in user_cart:
                if item['item_id'] == item_id:
                    item['quantity'] += quantity
                    break
            else:
                user_cart.append({
                    "item_id": item_id,
                    "quantity": quantity,
                    "price": item_price
                })

            return Response({"message": "Item added to cart", "cart": user_cart})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        return Response(CartData)


class CheckoutView(APIView):
    """
    API view to handle the checkout process for a user.

    POST:
        - Validates the request using CheckoutSerializer.
        - Calculates total, discount, and final amount based on user's cart and discount code.
        - Stores the order in the global Orders list.
        - Empties the user's cart.
        - Generates a new discount code every Nth order.
    """
    def post(self, request):
        """
        Handle POST request for order checkout.

        Returns:
            Response: A success message with order details and (conditionally) a new discount code.
        """
        global OrderCount
        global Orders

        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data["user_id"]
        discount_code_input = serializer.validated_data.get("discount_code")

        items = CartData[user_id]
        total_amount = sum(item["quantity"] * item["price"] for item in items)
        discount_amount = 0.0
        final_amount = total_amount
        code_used = None
        
        if discount_code_input:
            for code in DiscountCodes:
                discount_amount = total_amount * (DISCOUNT_PERCENTAGE / 100)
                final_amount = total_amount - discount_amount
                code["used"] = True
                code_used = code["code"]
                break

        OrderCount += 1
        order = {
            "order_id": f"order_{OrderCount}",
            "user_id": user_id,
            "items": items,
            "total_amount": total_amount,
            "discount_code_used": code_used,
            "discount_amount": discount_amount,
            "final_amount": final_amount
        }
        Orders.append(order)
        CartData[user_id] = []

        generated_code = None
        if OrderCount % NTH_ORDER == 0:
            new_code = generate_discount_code()
            DiscountCodes.append({
                "code": new_code,
                "used": False,
                "created_for_order_number": OrderCount
            })
            generated_code = new_code

        return Response({
            "message": "Checkout successful",
            "order": order,
            "new_discount_code_generated": generated_code
        })


class AdminStatsView(APIView):
    """
    API view for administrators to retrieve overall sales statistics.
    GET:
        - Calculates total number of items purchased across all orders.
        - Calculates the total purchase amount.
        - Calculates the total discount amount applied.
        - Returns all active and used discount codes.
    """
    def get(self, request):
        """
        Handle GET request to fetch administrative statistics.
        Returns:
            Response: A summary of platform-wide sales metrics including:
                - total_items_purchased: Sum of all item quantities across orders.
                - total_purchase_amount: Total revenue from all orders.
                - discount_codes: List of all discount codes and their usage status.
                - total_discount_amount: Total discounts applied across all orders.
        """
        total_items = sum(item["quantity"] for order in Orders for item in order["items"])
        total_purchase = sum(order["total_amount"] for order in Orders)
        total_discount = sum(order["discount_amount"] for order in Orders)

        return Response({
            "total_items_purchased": total_items,
            "total_purchase_amount": total_purchase,
            "discount_codes": DiscountCodes,
            "total_discount_amount": total_discount
        })


class AdminGenerateDiscountCodeView(APIView):
    """
    API view for administrators to generate a new discount code.
    POST:
        - Generates a unique discount code using a utility function.
        - Adds the code to the global DiscountCodes list with `used` set to False.
        - Returns the newly generated code in the response.
    """
    
    def post(self, request):
        """
        Handle POST request to generate a new discount code.
        Returns: Response: A success response containing the new discount code.
        """
        global DiscountCodes
        new_code = generate_discount_code()
        DiscountCodes.append({
            "code": new_code,
            "used": False,
            "created_for_order_number": None
        })
        return Response({"message": "Discount code generated.", "code": new_code})
    
    def get(self, request):
        return Response(DiscountCodes)


# Extra APIs:
class ItemListView(APIView):
    def get(self, request):
        return Response(Items)

class OrdersView(APIView):
    def get(self, request):
        return Response(Orders)
