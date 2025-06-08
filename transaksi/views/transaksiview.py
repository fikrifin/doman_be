import datetime
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from transaksi.models.transaksi import Transaksi
from transaksi.serializers.transaksiserializers import TransaksiSerializer

class TransaksiViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk CRUD Transaksi.
    Mendukung filter berdasarkan bulan dan tahun: /api/transaksi/?bulan=6&tahun=2025
    """
    serializer_class = TransaksiSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Transaksi.objects.filter(user=user)

        # Ambil parameter query untuk filtering
        bulan = self.request.query_params.get('bulan')
        tahun = self.request.query_params.get('tahun')

        if bulan and tahun:
            try:
                queryset = queryset.filter(tanggal__month=int(bulan), tanggal__year=int(tahun))
            except (ValueError, TypeError):
                # Abaikan jika parameter tidak valid
                pass
        
        return queryset.order_by('-tanggal', '-dibuat_pada')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)