from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib import auth
from apps.users.forms import (TravelUserRegisterForm, TravelUserEditForm,
                              TravelUserLoginForm)
from apps.carts.models import Cart
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


class LoginTravelUser(LoginView, GetAdditionalData):
    form_class = TravelUserLoginForm
    template_name = "users/login.html"
    extra_context = {"title": "Вход", "login": True}

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                obj = Cart.objects.filter(session_key=session_key)
                obj.update(user=user)
                obj.update(session_key=None)
                return HttpResponseRedirect(self.get_default_redirect_url())


class UserCartView(TemplateView, GetAdditionalData):
    template_name = "users/user_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "корзина"
        context["user_cart"] = True
        return context
