import datetime
from django.db import transaction
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
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
        
        return queryset.order_by('tanggal', '-dibuat_pada')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # --- IMPLEMENTASI BARU DI SINI ---
    @action(detail=False, methods=['get'], url_path='overview')
    def overview(self, request):
        """
        Custom action untuk menyediakan data komprehensif untuk halaman utama dasbor.
        URL: GET /api/transaksi/overview/
        """
        user = self.request.user
        today = datetime.date.today()
        
        # --- 1. Kalkulasi Ringkasan Bulan Ini ---
        transaksi_bulan_ini = self.get_queryset().filter(
            tanggal__year=today.year,
            tanggal__month=today.month
        )
        pemasukan_bulan_ini = transaksi_bulan_ini.filter(jenis=Transaksi.Jenis.PEMASUKAN).aggregate(
            total=Coalesce(Sum('jumlah'), 0, output_field=DecimalField())
        )['total']
        pengeluaran_bulan_ini = transaksi_bulan_ini.filter(jenis=Transaksi.Jenis.PENGELUARAN).aggregate(
            total=Coalesce(Sum('jumlah'), 0, output_field=DecimalField())
        )['total']
        
        # --- 2. Kalkulasi Ringkasan Keseluruhan ---
        semua_transaksi = self.get_queryset()
        pemasukan_total = semua_transaksi.filter(jenis=Transaksi.Jenis.PEMASUKAN).aggregate(
            total=Coalesce(Sum('jumlah'), 0, output_field=DecimalField())
        )['total']
        pengeluaran_total = semua_transaksi.filter(jenis=Transaksi.Jenis.PENGELUARAN).aggregate(
            total=Coalesce(Sum('jumlah'), 0, output_field=DecimalField())
        )['total']

        # --- 3. Ambil 10 Riwayat Transaksi Terakhir Bulan Ini ---
        riwayat_terakhir = transaksi_bulan_ini.order_by('-tanggal', '-dibuat_pada')[:10]
        riwayat_serializer = self.get_serializer(riwayat_terakhir, many=True)

        # --- 4. Susun Data Respons ---
        data = {
            'ringkasan_bulan_ini': {
                'total_pemasukan': pemasukan_bulan_ini,
                'total_pengeluaran': pengeluaran_bulan_ini,
                'sisa_saldo': pemasukan_bulan_ini - pengeluaran_bulan_ini,
            },
            'ringkasan_keseluruhan': {
                'total_pemasukan': pemasukan_total,
                'total_pengeluaran': pengeluaran_total,
                'sisa_saldo': pemasukan_total - pengeluaran_total,
            },
            'riwayat_terakhir': riwayat_serializer.data,
        }

        return Response(data)
