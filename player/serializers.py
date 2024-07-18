from rest_framework import serializers
from user.models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'user', 'name', 'age', 'rating', 'country']