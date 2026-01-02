from django.contrib import admin
from apps.users.models import TravelUser


class TravelUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email',
                    'is_superuser', 'is_active', 'age', ]


admin.site.register(TravelUser, TravelUserAdmin)
