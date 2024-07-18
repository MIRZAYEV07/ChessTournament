from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.schemas.openapi import AutoSchema
from django.core.cache import cache
from django.db.models import Q
from user.models import Player
from .serializers import PlayerSerializer
from typing import Any
import logging

logger = logging.getLogger(__name__)


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Any, view: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class PlayerListCreateAPIView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rating', 'country']
    search_fields = ['name', 'country']
    ordering_fields = ['rating', 'points']
    schema = AutoSchema()

    def get(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        players = cache.get('players')
        if players is None:
            queryset = Player.objects.all()
            queryset = self.filter_queryset(queryset)
            serializer = PlayerSerializer(queryset, many=True)
            players = serializer.data
            cache.set('players', players, 60 * 5)
        return Response(players)

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('players')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def filter_queryset(self, queryset):
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class PlayerDetailAPIView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request: Any, pk: int, *args: Any, **kwargs: Any) -> Response:
        cache_key = f"player_{pk}"
        player = cache.get(cache_key)
        if player is None:
            player = get_object_or_404(Player, pk=pk)
            serializer = PlayerSerializer(player)
            player = serializer.data
            cache.set(cache_key, player, 60 * 5)
        return Response(player)

    def put(self, request: Any, pk: int, *args: Any, **kwargs: Any) -> Response:
        player = get_object_or_404(Player, pk=pk)
        serializer = PlayerSerializer(player, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"player_{pk}")
            cache.delete("players")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Any, pk: int, *args: Any, **kwargs: Any) -> Response:
        player = get_object_or_404(Player, pk=pk)
        player.delete()
        cache.delete(f"player_{pk}")
        cache.delete("players")
        return Response(status=status.HTTP_204_NO_CONTENT)
