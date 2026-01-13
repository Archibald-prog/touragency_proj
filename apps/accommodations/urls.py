from django.urls import path
from apps.accommodations import views

urlpatterns = [
    path('', views.AccommodationListView.as_view(),
         name='main'),
    path('accommodations/<slug:slug>/', views.AccommodationDetailView.as_view(),
         name="accommodation_detail"),
]
