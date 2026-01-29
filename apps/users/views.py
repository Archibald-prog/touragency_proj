from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.users.forms import (TravelUserRegisterForm, TravelUserEditForm,
                              TravelUserLoginForm)
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
