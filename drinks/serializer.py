from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Drink
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class DrinkSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source='author_id.id')

    class Meta:
        model = Drink
        fields = ['id', 'name', 'description', 'author_id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            is_staff=validated_data.get('is_staff', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        return super().validate(credentials)