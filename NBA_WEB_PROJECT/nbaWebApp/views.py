from django.shortcuts import render
from rest_framework import generics
from .models import NBA_PLAYERS  # Adjust the import to match your actual model
from .serializers import NBAPlayerSerializer

def home(request):
    """
    Simple view to render the home page.
    """
    return render(request, 'home.html')

class NBAPlayerListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating NBA players.
    """
    queryset = NBA_PLAYERS.objects.all()  # Adjust model name if necessary
    serializer_class = NBAPlayerSerializer
