import datetime
from django.db import transaction
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from transaksi.models.rekening import Rekening
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

        bulan = self.request.query_params.get('bulan')
        tahun = self.request.query_params.get('tahun')

        if bulan and tahun:
            try:
                queryset = queryset.filter(tanggal__month=int(bulan), tanggal__year=int(tahun))
            except (ValueError, TypeError):
                pass
        
        return queryset.order_by('-tanggal', '-dibuat_pada')

    def perform_create(self, serializer):
        rekening = serializer.validated_data['rekening']
        jumlah = serializer.validated_data['jumlah']
        jenis = serializer.validated_data['jenis']

        if rekening.user != self.request.user:
            raise serializers.ValidationError("Anda tidak memiliki akses ke rekening ini.")

        with transaction.atomic():
            rekening_locked = Rekening.objects.select_for_update().get(pk=rekening.pk)
            
            if jenis == Transaksi.Jenis.PEMASUKAN:
                rekening_locked.saldo += jumlah
            else:
                rekening_locked.saldo -= jumlah
            
            rekening_locked.save()
            serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        rekening_lama = instance.rekening
        jumlah_lama = instance.jumlah
        jenis_lama = instance.jenis

        rekening_baru = serializer.validated_data.get('rekening', rekening_lama)
        jumlah_baru = serializer.validated_data.get('jumlah', jumlah_lama)
        jenis_baru = serializer.validated_data.get('jenis', jenis_lama)

        if rekening_baru.user != self.request.user:
            raise serializers.ValidationError("Anda tidak memiliki akses ke rekening ini.")

        with transaction.atomic():
            rekening_lama_locked = Rekening.objects.select_for_update().get(pk=rekening_lama.pk)
            if jenis_lama == Transaksi.Jenis.PEMASUKAN:
                rekening_lama_locked.saldo -= jumlah_lama
            else:
                rekening_lama_locked.saldo += jumlah_lama
            rekening_lama_locked.save()
            
            rekening_baru_locked = Rekening.objects.select_for_update().get(pk=rekening_baru.pk)
            if jenis_baru == Transaksi.Jenis.PEMASUKAN:
                rekening_baru_locked.saldo += jumlah_baru
            else:
                rekening_baru_locked.saldo -= jumlah_baru
            rekening_baru_locked.save()
            
            serializer.save()

    def perform_destroy(self, instance):
        rekening = instance.rekening
        jumlah = instance.jumlah
        jenis = instance.jenis

        with transaction.atomic():
            rekening_locked = Rekening.objects.select_for_update().get(pk=rekening.pk)
            if jenis == Transaksi.Jenis.PEMASUKAN:
                rekening_locked.saldo -= jumlah
            else:
                rekening_locked.saldo += jumlah
            rekening_locked.save()
            instance.delete()

    @action(detail=False, methods=['get'], url_path='overview')
    def overview(self, request):
        """
        Custom action untuk menyediakan data komprehensif untuk halaman utama dasbor.
        URL: GET /api/transaksi/overview/
        """
        user = self.request.user
        today = datetime.date.today()
        
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
        
        semua_transaksi = self.get_queryset()
        pemasukan_total = semua_transaksi.filter(jenis=Transaksi.Jenis.PEMASUKAN).aggregate(
            total=Coalesce(Sum('jumlah'), 0, output_field=DecimalField())
        )['total']
        pengeluaran_total = semua_transaksi.filter(jenis=Transaksi.Jenis.PENGELUARAN).aggregate(
            total=Coalesce(Sum('jumlah'), 0, output_field=DecimalField())
        )['total']

        riwayat_terakhir = transaksi_bulan_ini.order_by('-tanggal', '-dibuat_pada')[:10]
        riwayat_serializer = self.get_serializer(riwayat_terakhir, many=True)

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
