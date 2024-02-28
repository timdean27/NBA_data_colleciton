# serializers.py
from rest_framework import serializers
from .models import NBA_PLAYERS

class NBAPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBA_PLAYERS
        fields = '__all__'
