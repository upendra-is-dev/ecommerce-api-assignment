from rest_framework.test import APITestCase
from django.urls import reverse

# Import mock data if available
from .constraints.globals import Users, Items, CartData, DiscountCodes, Orders, OrderCount, NTH_ORDER

class StoreAPITests(APITestCase):
    def setUp(self):
        # Reset shared global states before each test
        Users.clear()
        Items.clear()
        CartData.clear()
        DiscountCodes.clear()
        Orders.clear()
        global OrderCount
        OrderCount = 0

        # Setup mock users and items
        Users['user_1'] = {"name": "Alice"}
        Items['item_1'] = {"name": "Product A", "price": 100}
        Items['item_2'] = {"name": "Product B", "price": 200}

    def test_add_to_cart_success(self):
        url = reverse('add-to-cart')
        data = {
            "user_id": "user_1",
            "item_id": "item_1",
            "quantity": 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Item added to cart", response.data["message"])
        self.assertEqual(len(CartData["user_1"]), 1)
        self.assertEqual(CartData["user_1"][0]["quantity"], 2)

    def test_add_to_cart_invalid_user(self):
        url = reverse('add-to-cart')
        data = {
            "user_id": "invalid_user",
            "item_id": "item_1",
            "quantity": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid user.", str(response.data))

    def test_checkout_without_discount(self):
        # First add item to cart
        CartData['user_1'] = [{"item_id": "item_1", "quantity": 2, "price": 100}]
        url = reverse('checkout')
        data = {
            "user_id": "user_1"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Checkout successful", response.data["message"])
        self.assertEqual(response.data["order"]["total_amount"], 200)
        self.assertEqual(CartData['user_1'], [])  # Cart should be cleared

    def test_checkout_with_invalid_discount(self):
        # Add to cart
        CartData['user_1'] = [{"item_id": "item_1", "quantity": 1, "price": 100}]
        url = reverse('checkout')
        data = {
            "user_id": "user_1",
            "discount_code": "FAKECODE"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid or already used discount code", str(response.data))

    def test_checkout_with_valid_discount(self):
        # Setup
        CartData['user_1'] = [{"item_id": "item_1", "quantity": 1, "price": 100}]
        DiscountCodes.append({"code": "VALID10", "used": False, "created_for_order_number": None})

        url = reverse('checkout')
        data = {
            "user_id": "user_1",
            "discount_code": "VALID10"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["order"]["discount_amount"], 10.0)  # 10% of 100
        self.assertTrue(DiscountCodes[0]["used"])  # Code should be marked as used

    def test_admin_generate_discount_code(self):
        url = reverse('admin-generate-discount')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("code", response.data)
        self.assertEqual(len(DiscountCodes), 1)

    def test_admin_stats(self):
        # Add mock order
        Orders.append({
            "order_id": "order_1",
            "user_id": "user_1",
            "items": [{"item_id": "item_1", "quantity": 2, "price": 100}],
            "total_amount": 200,
            "discount_code_used": None,
            "discount_amount": 0,
            "final_amount": 200
        })
        url = reverse('admin-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_items_purchased"], 2)
        self.assertEqual(response.data["total_purchase_amount"], 200)
