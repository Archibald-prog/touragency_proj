# from decimal import Decimal
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.accommodations.models import AccommodationAvailability
from apps.helpers import GetAdditionalData
from apps.carts.models import Cart
from apps.orders.forms import CreateOrderForm
from apps.orders.models import Order, OrderItem


class CreateOrderView(LoginRequiredMixin, FormView,
                      GetAdditionalData):
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy('main')
    success_message = None

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                        email=form.cleaned_data['email'],
                    )
                    for cart_item in cart_items:
                        accommodation = cart_item.accommodation
                        name = cart_item.accommodation.name
                        roomclass = cart_item.room_class
                        nights = cart_item.nights
                        guests = cart_item.guests
                        price = cart_item.accommodation_cost

                        obj = AccommodationAvailability.objects.get(
                            accommodation_id=accommodation.pk,
                            room_class_id=roomclass.pk
                        )

                        if obj.availability < 1:
                            raise ValidationError(
                                f"Нет свободных номеров класса {roomclass}")

                        OrderItem.objects.create(
                            order=order,
                            accommodation=accommodation,
                            name=name,
                            nights=nights,
                            guests=guests,
                            price=price,
                        )
                        obj.availability -= 1
                        obj.save()

                    cart_items.delete()
                    messages.success(self.request, 'Заказ оформлен:)')
                    return redirect('main')
        except ValidationError as e:
            messages.warning(self.request, *e)
            return redirect('orders:create_order')

    def form_invalid(self, form):
        messages.warning(self.request,
                         'Заполните все обязательные поля!')
        return redirect('orders:create_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформление заказа"
        context["orders"] = True
        return context
