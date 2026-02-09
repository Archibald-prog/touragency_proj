from django.template.loader import render_to_string
from apps.helpers import GetAdditionalData
from apps.carts.models import Cart


class CartMixin(GetAdditionalData):
    def get_cart_accommodation(self, request, accommodation=None, cart_id=None):
        query_kwargs = {}
        if request.user.is_authenticated:
            query_kwargs["user"] = request.user
        if accommodation:
            query_kwargs["accommodation"] = accommodation
        if cart_id:
            query_kwargs["id"] = cart_id
        return Cart.objects.filter(**query_kwargs).first()

    def render_cart(self, request):
        """
        Returns an updated version
        of the cart html markup.
        """
        user_cart = self.get_user_cart(request)
        roomclasses = self.get_roomclasses()
        context = {"carts": user_cart, "roomclasses": roomclasses}

        return render_to_string(
            "carts/includes/inc_cart_list.html",
            context, request=request)

    def get_response_data(self, request):
        total_tours = Cart.objects.filter(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key
            if not request.user.is_authenticated else None
        ).total_tours()

        response_data = {
            "total_tours": total_tours,
            "cart_items_html": self.render_cart(request),
        }
        return response_data
