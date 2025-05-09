from django.urls import path
from .views import ItemListView, AddToCartView, CheckoutView, AdminStatsView, AdminGenerateDiscountCodeView, OrdersView

urlpatterns = [
    path("items/", ItemListView.as_view(), name="items"),
    path("orders/", OrdersView.as_view(), name="order"),
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("admin/stats/", AdminStatsView.as_view(), name="admin-stats"),
    path("admin/generate-discount/", AdminGenerateDiscountCodeView.as_view(), name="admin-generate-discount")
]