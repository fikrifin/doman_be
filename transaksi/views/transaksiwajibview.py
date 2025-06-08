import datetime
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from transaksi.models.transaksiwajib import TransaksiWajib
from transaksi.serializers.transaksiwajibserializers import TransaksiWajibSerializer

class TransaksiWajibViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk CRUD template Transaksi Wajib.
    """
    serializer_class = TransaksiWajibSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TransaksiWajib.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)