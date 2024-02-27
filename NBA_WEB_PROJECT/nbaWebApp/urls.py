from django.urls import path
from .views import NBAPlayerListCreateView

urlpatterns = [
    path('api/players/', NBAPlayerListCreateView.as_view(), name='player-list-create'),
]
