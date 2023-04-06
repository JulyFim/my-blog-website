from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

# models & serializers
from django.contrib.auth.models import User
from blog import models
from . import serializers


# permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny, IsAuthenticated


# filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class UserViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filter_fields = ['first_name', 'last_name', 'username', 'email']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    ordering_fields = ['id', 'first_name', 'last_name', 'username']


class CategoryViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filter_fields = ['title', 'slug']
    search_fields = ['title', 'slug']
    ordering_fields = ['title', 'slug']


class PostViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filter_fields = ['title', 'slug', 'author', 'tag', 'category', 'created_on', 'last_update']
    search_fields = ['title', 'slug', 'author']
    ordering_fields = ['author', 'tag', 'category', 'created_on', 'last_update']


class UserProfileViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)

    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filter_fields = ['id', 'user', 'username', 'address']
    search_fields = ['user', 'username', 'bio', 'address']
    ordering_fields = ['id', 'user', 'created_on']


class LoginApiView(APIView):
    permission_classes = (AllowAny, )

    @staticmethod
    def post(request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.save()

        return Response({"key": token.key})


class LogOutApiView(APIView):
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def post(request):
        request.user.auth_token.delete()
        return Response({"info": "Logged out successfully!"})


class RegisterApiView(APIView):
    permission_classes = (AllowAny, )

    @staticmethod
    def post(request):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"info": "Registered successfully!"})
