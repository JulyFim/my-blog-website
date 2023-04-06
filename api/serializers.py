from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from blog import models
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name', 'last_name',
                  'email',
                  'is_staff', 'is_active', 'is_superuser',
                  'groups', 'user_permissions',
                  'date_joined', 'last_login'
                  )
        read_only_fields = ('id', 'date_joined')
        write_only_fields = ('password', )


class CategorySerializer(ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'
        read_only_fields = ('id',)


class PostSerializer(ModelSerializer):
    author = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = models.Post
        fields = '__all__'
        read_only_fields = ('id', 'author')


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.UserProfile
        fields = '__all__'
        read_only_fields = ('id', 'created_on')


class LoginSerializer(ModelSerializer):
    username = serializers.CharField(max_length=60)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError({"error": "There is no such a user"})

        return super().validate(attrs)

    def create(self, validated_data):
        username = validated_data.get('username')

        user = User.objects.get(username=username)
        token = Token.objects.create(user=user)

        return token


class RegisterSerializer(ModelSerializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(min_length=8, max_length=128)
    password2 = serializers.CharField(min_length=8, max_length=128)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if password2 != password1:
            raise ValidationError({"error": "Password didn't match"})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user.set_password(validated_data.get('password1'))
        user.save()

        return user
