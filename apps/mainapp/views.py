from django.views.generic import ListView, TemplateView
from apps.mainapp.models import Contact
from apps.helpers import GetAdditionalData


class ConactListView(ListView, GetAdditionalData):
    model = Contact
    template_name = 'mainapp/contact_list.html'
    extra_context = {"title": "Контакты", "contact": True}


class PartnerView(TemplateView, GetAdditionalData):
    template_name = 'mainapp/partner.html'
    extra_context = {"title": "Партнерам", "partner": True}
