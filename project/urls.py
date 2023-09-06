from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from project import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('adverts/', include('adverts.urls')),
    path('accounts/', include('accounts.urls')),
]
