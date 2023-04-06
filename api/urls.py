from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='users')
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'posts', views.PostViewSet, basename='posts')
router.register(r'user_profiles', views.UserProfileViewSet, basename='user_profiles')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('logout/', views.LogOutApiView.as_view(), name='logout'),
    path('register/', views.RegisterApiView.as_view(), name='register')
]
