from django.urls import path
from django.contrib.auth.views import LogoutView
import apps.users.views as users

app_name = 'users'

urlpatterns = [
    path('login/', users.LoginTravelUser.as_view(),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='auth:login'),
         name='logout'),
    path('register/', users.RegisterTravelUser.as_view(),
         name='register'),
    path('edit/', users.EditTravelUser.as_view(),
         name='edit'),
    path('user-cart/', users.UserCartView.as_view(),
         name='user_cart'),
]
