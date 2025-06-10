import datetime
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from transaksi.models.kategori import Kategori
from transaksi.serializers.kategoriserializers import KategoriSerializer

class KategoriViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk CRUD Kategori.
    """
    serializer_class = KategoriSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Hanya tampilkan kategori milik user yang sedang login
        return Kategori.objects.filter(user=self.request.user).order_by('nama')

    def perform_create(self, serializer):
        # Saat kategori baru dibuat, otomatis set user-nya
        serializer.save(user=self.request.user)