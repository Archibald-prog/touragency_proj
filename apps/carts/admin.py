from django.contrib import admin
from apps.carts.models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ("accommodation", "room_class", "guests", "nights", "add_datetime", )
    readonly_fields = ("add_datetime", )
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user_display", "accommodation", "room_class", "nights",
                    "guests", "add_datetime", ]
    list_filter = ["add_datetime", "user", "accommodation__name", ]


    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"
