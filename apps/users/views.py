from django.db.models import Prefetch
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import resolve_url
from django.conf import settings
from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView
from django.contrib import auth, messages
from apps.users.forms import (TravelUserRegisterForm, TravelUserEditForm,
                              TravelUserLoginForm)
from apps.carts.models import Cart
from apps.orders.models import Order, OrderItem
from apps.helpers import GetAdditionalData


class RegisterTravelUser(CreateView, GetAdditionalData):
    form_class = TravelUserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("auth:login")
    extra_context = {"title": "Регистрация",
                     "register": True}


class EditTravelUser(UpdateView, GetAdditionalData):
    form_class = TravelUserEditForm
    template_name = "users/edit.html"
    success_url = reverse_lazy("main")
    extra_context = {"title": "Редактирование профиля",
                     "edit": True}

    def get_object(self, *args, **kwargs):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Аккаунт успешно обновлен")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)


class LoginTravelUser(LoginView, GetAdditionalData):
    form_class = TravelUserLoginForm
    template_name = "users/login.html"
    extra_context = {"title": "Вход", "login": True}

    def get_default_redirect_url(self):
        if 'orders' in self.request.META.get('HTTP_REFERER'):
            self.next_page = reverse('orders:create_order')
            return resolve_url(self.next_page)
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                obj = Cart.objects.filter(session_key=session_key)
                obj.update(user=user)
                obj.update(session_key=None)
                messages.success(self.request, f"{user.first_name}, вы вошли в аккаунт")
                return HttpResponseRedirect(self.get_default_redirect_url())


class UserCartView(TemplateView, GetAdditionalData):
    template_name = "users/user_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "корзина"
        context["user_cart"] = True
        return context


class UserProfileView(ListView, GetAdditionalData):
    template_name = "users/user_profile.html"
    context_object_name = 'orders'

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("accommodation"),
            )
        ).order_by("-id")
        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "профиль пользователя"
        context["user_profile"] = True
        return context
