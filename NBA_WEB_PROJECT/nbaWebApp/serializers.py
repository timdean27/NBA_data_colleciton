# serializers.py
from rest_framework import serializers
from .models import nba_players

class NBAPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = nba_players
        fields = '__all__'
