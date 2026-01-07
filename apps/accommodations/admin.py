from django.contrib import admin
from apps.accommodations.models import (Country, Region, Accommodation,
                                        AccommodationImage, RoomClass,
                                        AccommodationCost, AccommodationAvailability,
                                        AccommodationFeatures)

admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Accommodation)
admin.site.register(AccommodationImage)
admin.site.register(RoomClass)
admin.site.register(AccommodationCost)
admin.site.register(AccommodationAvailability)
admin.site.register(AccommodationFeatures)
