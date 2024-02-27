from django.shortcuts import render
from rest_framework import generics
from .models import nba_players  # Adjust the import to match your actual model
from .serializers import NBAPlayerSerializer

def home(request):
    return render(request, 'home.html') 

class NBAPlayerListCreateView(generics.ListCreateAPIView):
    queryset = nba_players.objects.all()
    serializer_class = NBAPlayerSerializer
