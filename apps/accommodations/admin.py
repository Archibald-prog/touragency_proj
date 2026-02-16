from django.contrib import admin
from apps.accommodations.models import (Country, Region, Accommodation,
                                        AccommodationImage, RoomClass,
                                        AccommodationCost, AccommodationAvailability,
                                        AccommodationFeatures)

admin.site.register(Region)
admin.site.register(AccommodationImage)
admin.site.register(RoomClass)
admin.site.register(AccommodationCost)
admin.site.register(AccommodationAvailability)
admin.site.register(AccommodationFeatures)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", ]


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "region"]
    search_fields = ["name", "description", "country__name", "region__name"]
    list_filter = ["country", "region"]
    fields = [
        "name",
        "country",
        "region",
        "slug",
        "description",
        "flight_cost_per_one",
        "old_price",
        "is_top",
        "is_new",
        "is_active",
    ]
