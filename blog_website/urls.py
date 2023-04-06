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
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as drf_schema_view
from drf_yasg import openapi

schema_view = drf_schema_view(
    openapi.Info(
        title='Xtra Blog API',
        default_version='v1',
        terms_of_service='https://www.google.com/police/terms/',
        contact=openapi.Contact(email='ahmedovbahtiar55@gmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('', include('blog.urls')),
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
    # documentation
    path('schema/', get_schema_view(
        title='Plumbing-Gas-Installation API',
        description='API Description',
        version='1.0.0'
    ),
         name='openapi-schema'
         ),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-doc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc')
]
