from django.shortcuts import render
from rest_framework import generics
from .models import NBA_PLAYERS  # Adjust the import to match your actual model
from .serializers import NBAPlayerSerializer

def home(request):
    return render(request, 'home.html') 

class NBAPlayerListCreateView(generics.ListCreateAPIView):
    queryset = NBA_PLAYERS.objects.all()
    serializer_class = NBAPlayerSerializer
