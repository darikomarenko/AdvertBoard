from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from allauth.account import views as allauth_views

from project import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('adverts/', include('adverts.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("accounts/logout/", allauth_views.LogoutView.as_view(), name="logout"),
    path("accounts/login/", allauth_views.LoginView.as_view(), name="login"),
    path("accounts/signup/", allauth_views.SignupView.as_view(), name="signup"),
]
