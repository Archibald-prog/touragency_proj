from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("apps.accommodations.urls")),
    path('auth/', include("apps.users.urls", namespace="auth")),
    path('cart/', include("apps.carts.urls", namespace="cart")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
