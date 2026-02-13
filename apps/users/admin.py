from django.contrib import admin
from apps.users.models import TravelUser
from apps.orders.admin import OrderTabAdmin
from apps.carts.admin import CartTabAdmin

@admin.register(TravelUser)
class TravelUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email',
                    'is_superuser', 'is_active', 'age', ]
    search_fields = ['username', 'first_name', 'last_name', 'email', ]
    inlines = [CartTabAdmin, OrderTabAdmin]
