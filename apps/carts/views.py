from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic.base import View
from apps.carts.models import Cart
from apps.accommodations.models import Accommodation
from apps.carts.mixins import CartMixin


class CartAdd(CartMixin, View):
    def post(self, request):
        accommodation_id = request.POST.get("accommodation_id")
        accommodation = get_object_or_404(Accommodation, id=accommodation_id)

        cart = self.get_cart_accommodation(request,
                                           accommodation=accommodation)

        if cart:
            cart.nights += 4
            cart.save()
        else:
            Cart.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key
                if not request.user.is_authenticated else None,
                accommodation=accommodation, nights=3
            )
        response_data = {
            'cart_items_html': self.render_cart(request)
        }
        return JsonResponse(response_data)


class CartRemove(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart_record = get_object_or_404(Cart, pk=cart_id)
        cart_record.delete()
        quantity_deleted = 1

        response_data = {
            "quantity_deleted": quantity_deleted,
            "cart_items_html": self.render_cart(request)
        }
        return JsonResponse(response_data)


class RoomclassEdit(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart_item = Cart.objects.get(pk=int(cart_id))

        item_roomclass = request.POST.get("roomclass")
        if item_roomclass:
            cart_item.room_class_id = item_roomclass
            cart_item.save()

        response_data = self.get_response_data(request)
        return JsonResponse(response_data)


class GuestNumEdit(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart_item = Cart.objects.get(pk=int(cart_id))

        item_guests = request.POST.get("guests")
        if item_guests:
            cart_item.guests = item_guests
            cart_item.save()

        response_data = self.get_response_data(request)
        return JsonResponse(response_data)


class NightNumEdit(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart_item = Cart.objects.get(pk=int(cart_id))

        item_nights = request.POST.get("nights")
        if item_nights:
            cart_item.nights = item_nights
            cart_item.save()

        response_data = self.get_response_data(request)
        return JsonResponse(response_data)
