from django.contrib import admin
from .models import (
    Category, Product, CustomerAddress, Order, OrderItem, Restaurant,
    DeliveryPerson, Payment, OrderTracking, ProductReview, UserProfile,
    Coupon, OrderStatusHistory, Favorite, SupportTicket, RestaurantHours
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'restaurant']
    list_filter = ['category', 'restaurant']
    search_fields = ['name', 'description']

@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'label', 'city', 'pincode', 'is_default']
    list_filter = ['city', 'is_default']
    search_fields = ['user__username', 'address', 'pincode']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created_at']
    search_fields = ['name']

@admin.register(DeliveryPerson)
class DeliveryPersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone', 'is_available']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'method', 'status', 'transaction_id']

@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'current_status', 'updated_at']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'rating', 'created_at']
    list_filter = ['rating']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'role']
    list_filter = ['role']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'discount_amount', 'valid_from', 'valid_to', 'is_active']
    list_filter = ['is_active']

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'status', 'timestamp']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'added_at']

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject', 'is_resolved', 'created_at']
    list_filter = ['is_resolved']

@admin.register(RestaurantHours)
class RestaurantHoursAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'day_of_week', 'opens_at', 'closes_at']
