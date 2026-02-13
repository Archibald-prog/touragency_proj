from django.contrib import admin
from apps.orders.models import Order, OrderItem


class OrderTabAdmin(admin.TabularInline):
    model = Order
    fields = ("phone_number", "status", "payment_on_get",
              "created_timestamp", "is_paid",)
    readonly_fields = ("created_timestamp",)
    extra = 1


class OrderItemTabAdmin(admin.TabularInline):
    model = OrderItem
    fields = ("name", "nights", "price", )
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_number", "is_paid", "payment_on_get",
                    "status", "created_timestamp", ]
    list_filter = ["user", "phone_number", "created_timestamp", ]
    search_fields = ["user_name", "phone_number"]
    inlines = [OrderItemTabAdmin]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "accommodation", "name", "price",
                    "created_timestamp", ]
    list_filter = ["order", "created_timestamp", ]
    search_fields = ["name", "created_timestamp"]
