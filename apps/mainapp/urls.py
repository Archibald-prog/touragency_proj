from django.urls import path
import apps.mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('contact/', mainapp.ConactListView.as_view(), name="contact"),
    path('partner/', mainapp.PartnerView.as_view(), name="partner"),
]
