from rest_framework import serializers
from django.contrib.auth.models import User
from ...models import Drink
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

