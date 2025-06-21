from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Product, CustomerAddress, Order, OrderItem, Restaurant,
    DeliveryPerson, Payment, OrderTracking, ProductReview, UserProfile,
    Coupon, OrderStatusHistory, Favorite, SupportTicket, RestaurantHours, CartItem, Cart
)

class OTPRequestSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)

class OTPVerifySerializer(serializers.Serializer):
    mobile = serializers.CharField()
    otp = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'is_active', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'category', 'restaurant']


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = [
            'id', 'user', 'label', 'address', 'city', 'pincode',
            'latitude', 'longitude', 'is_default'
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    address = CustomerAddressSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'status', 'total_price', 'created_at', 'items']


class DeliveryPersonSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DeliveryPerson
        fields = ['id', 'user', 'is_available', 'phone', 'current_location']


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'order', 'method', 'status', 'transaction_id', 'created_at']


class OrderTrackingSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderTracking
        fields = ['id', 'order', 'current_status', 'updated_at']


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_amount', 'valid_from', 'valid_to', 'is_active']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'order', 'status', 'timestamp']


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'added_at']


class SupportTicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = SupportTicket
        fields = ['id', 'user', 'subject', 'message', 'is_resolved', 'created_at']


class RestaurantHoursSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = RestaurantHours
        fields = ['id', 'restaurant', 'day_of_week', 'opens_at', 'closes_at']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

