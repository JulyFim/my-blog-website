"""blog_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproj

You’re seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard 404 page.
ect.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('api/v1/', include('api.urls')),
    # password reset
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='password/reset_done.html'
    ),
         name='password_reset_done'
         ),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='password/reset_confirm.html'
    ),
         name='password_reset_confirm'
         ),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(
        template_name='password/reset_complete.html'
    ),
         name='password_reset_complete'
         ),
]
