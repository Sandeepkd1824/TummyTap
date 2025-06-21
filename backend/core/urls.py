from django.urls import path
from .views import (
    CategoryListAPIView, ProductListAPIView, CartView, AddToCartView,
    RemoveFromCartView, CustomerAddressListCreateView, PlaceOrderView,
    OrderListView, ProductReviewCreateView, FavoriteToggleView,
    ApplyCouponView, RequestOTPView, VerifyOTPView
)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),

    path('cart/', CartView.as_view(), name='cart-view'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='cart-remove'),

    path('addresses/', CustomerAddressListCreateView.as_view(), name='address-list-create'),

    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/place/', PlaceOrderView.as_view(), name='order-place'),

    path('reviews/add/', ProductReviewCreateView.as_view(), name='review-add'),
    path('favorites/toggle/', FavoriteToggleView.as_view(), name='favorite-toggle'),

    path('coupons/apply/', ApplyCouponView.as_view(), name='coupon-apply'),

    path('auth/request-otp/', RequestOTPView.as_view()),
    path('auth/verify-otp/', VerifyOTPView.as_view()),
]
