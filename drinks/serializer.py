from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Drink
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Drink

class DrinkSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source='author_id.id')  # Update this line
    image = serializers.ImageField(required=False)
    vote_count = serializers.IntegerField(read_only=True)  # Include vote count field

    class Meta:
        model = Drink
        fields = ['id', 'name', 'description', 'author_id', 'image', 'vote_count']

    def create(self, validated_data):
        image_data = validated_data.pop('image', None)
        drink = Drink.objects.create(**validated_data)

        if image_data:
            drink.image = image_data
            drink.save()

        return drink


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