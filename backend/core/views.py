from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


import random
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OTPRequest
from .serializers import OTPRequestSerializer, OTPVerifySerializer, UserSerializer

from .models import (
    Category, Product, Cart, CartItem, Order, OrderItem, CustomerAddress,
    ProductReview, Coupon, Favorite
)
from .serializers import (
    CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer,
    OrderSerializer, OrderItemSerializer, CustomerAddressSerializer,
    ProductReviewSerializer
)


# ---------- CATEGORY ----------
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ---------- PRODUCTS ----------
class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get("category_id")
        search = self.request.query_params.get("search")

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


# ---------- CART ----------
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)
        product = get_object_or_404(Product, id=product_id)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)

        cart_item.save()
        return Response({"message": "Item added to cart"})


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        cart = get_object_or_404(Cart, user=request.user)
        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

        if item:
            item.delete()
            return Response({"message": "Item removed"})
        return Response({"message": "Item not found"}, status=404)


# ---------- CUSTOMER ADDRESSES ----------
class CustomerAddressListCreateView(generics.ListCreateAPIView):
    serializer_class = CustomerAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------- ORDERS ----------
class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        address_id = request.data.get("address_id")
        address = get_object_or_404(CustomerAddress, id=address_id, user=request.user)
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()

        if not cart_items:
            return Response({"message": "Cart is empty"}, status=400)

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, address=address, total_price=total_price)

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        cart_items.delete()

        return Response({"message": "Order placed successfully", "order_id": order.id})


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


# ---------- REVIEWS ----------
class ProductReviewCreateView(generics.CreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------- FAVORITES ----------
class FavoriteToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        fav, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            fav.delete()
            return Response({"message": "Removed from favorites"})
        return Response({"message": "Added to favorites"})


# ---------- COUPON CHECK ----------
class ApplyCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            return Response({
                "valid": True,
                "discount": coupon.discount_amount
            })
        except Coupon.DoesNotExist:
            return Response({
                "valid": False,
                "message": "Invalid or expired coupon"
            }, status=400)


def send_otp_mock(mobile, otp):
    print(f"Sending OTP {otp} to {mobile}")  # In real app: call Twilio, MSG91, etc.

class RequestOTPView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            otp = f"{random.randint(100000, 999999)}"
            otp_entry, _ = OTPRequest.objects.update_or_create(
                mobile=mobile,
                defaults={'otp': otp, 'is_verified': False}
            )
            send_otp_mock(mobile, otp)
            return Response({'message': 'OTP sent successfully'}, status=200)
        return Response(serializer.errors, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            otp = serializer.validated_data['otp']
            try:
                otp_entry = OTPRequest.objects.get(mobile=mobile, otp=otp)
                if otp_entry.is_expired():
                    return Response({'error': 'OTP expired'}, status=400)

                otp_entry.is_verified = True
                otp_entry.save()

                user, _ = User.objects.get_or_create(username=mobile)
                refresh = RefreshToken.for_user(user)

                return Response({
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            except OTPRequest.DoesNotExist:
                return Response({'error': 'Invalid OTP'}, status=400)
        return Response(serializer.errors, status=400)
