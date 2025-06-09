import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from transaksi.models import (Tagihan, StatusTagihan, Transaksi)
from transaksi.serializers.tagihanserializers import TagihanSerializer

class ChecklistWajibViewSet(viewsets.ViewSet):
    """
    API endpoint untuk melihat checklist transaksi wajib dan menandainya sebagai lunas.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Mengembalikan daftar semua transaksi wajib untuk bulan ini,
        beserta status pembayarannya (lunas/belum).
        URL: /api/checklist/
        """
        today = datetime.date.today()
        bulan, tahun = today.month, today.year
        
        # Ambil semua template transaksi wajib yang aktif
        queryset = Tagihan.objects.filter(user=request.user, aktif=True)
        
        response_data = []
        for tw in queryset:
            # Cek status pembayarannya untuk bulan ini
            status_obj = StatusTagihan.objects.filter(
                transaksi_wajib=tw, bulan=bulan, tahun=tahun
            ).first()
            
            data = TagihanSerializer(tw).data
            data['status_lunas'] = status_obj.status_lunas if status_obj else False
            response_data.append(data)
            
        return Response(response_data)

    @action(detail=True, methods=['post'], url_path='bayar')
    @transaction.atomic
    def tandai_lunas(self, request, pk=None):
        """
        Menandai transaksi wajib sebagai lunas untuk bulan ini.
        Secara otomatis akan membuat record Transaksi baru.
        URL: POST /api/checklist/{id}/bayar/
        """
        transaksi_wajib = Tagihan.objects.get(pk=pk, user=request.user)
        
        today = datetime.date.today()
        bulan, tahun = today.month, today.year

        status_pembayaran, created = StatusTagihan.objects.get_or_create(
            transaksi_wajib=transaksi_wajib, bulan=bulan, tahun=tahun
        )

        if status_pembayaran.status_lunas:
            return Response(
                {'error': 'Transaksi ini sudah ditandai lunas.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buat transaksi pengeluaran baru
        transaksi_baru = Transaksi.objects.create(
            user=request.user,
            kategori=transaksi_wajib.kategori,
            deskripsi=transaksi_wajib.deskripsi,
            jumlah=transaksi_wajib.jumlah_estimasi,
            jenis=Transaksi.Jenis.PENGELUARAN,
            tanggal=today
        )

        # Update status
        status_pembayaran.status_lunas = True
        status_pembayaran.transaksi_pembayaran = transaksi_baru
        status_pembayaran.save()

        return Response(
            {'status': 'success', 'message': f"'{transaksi_wajib.deskripsi}' telah ditandai lunas."},
            status=status.HTTP_200_OK
        )