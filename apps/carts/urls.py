from django.urls import path
import apps.carts.views as carts

app_name = "carts"

urlpatterns = [
    path('add/', carts.CartAdd.as_view(), name="add"),
    path('remove/', carts.CartRemove.as_view(), name="remove"),
    path('roomclass-edit/', carts.RoomclassEdit.as_view(),
         name="roomclass_edit"),
    path('guest-edit/', carts.GuestNumEdit.as_view(), name="guest_edit"),
    path('night-edit/', carts.NightNumEdit.as_view(), name="night_edit"),
]
