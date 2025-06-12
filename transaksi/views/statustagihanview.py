import datetime
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from transaksi.models.tagihan import Tagihan
from transaksi.models.statustagihan import StatusTagihan
from transaksi.models.rekening import Rekening
from transaksi.models.transaksi import Transaksi

from transaksi.serializers.tagihanserializers import TagihanSerializer

class StatusTagihanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint untuk melihat checklist tagihan dan menandainya sebagai lunas.
    Menggantikan ChecklistWajibViewSet.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TagihanSerializer

    def get_queryset(self):
        """
        Queryset dasar adalah semua template Tagihan yang aktif milik user.
        """
        return Tagihan.objects.filter(user=self.request.user, aktif=True).order_by('hari_jatuh_tempo')

    def list(self, request, *args, **kwargs):
        """
        Mengembalikan daftar checklist untuk bulan berjalan.
        Untuk setiap template Tagihan, ia akan mencari atau membuat statusnya
        untuk bulan ini dan menggabungkan informasinya.
        URL: GET /api/status-tagihan/
        """
        queryset = self.get_queryset()
        today = datetime.date.today()
        bulan, tahun = today.month, today.year

        response_data = []
        for tagihan in queryset:
            status_obj, created = StatusTagihan.objects.get_or_create(
                tagihan=tagihan,
                bulan=bulan,
                tahun=tahun
            )
            
            data = self.get_serializer(tagihan).data
            data['status_lunas'] = status_obj.status_lunas
            response_data.append(data)
            
        return Response(response_data)

    @action(detail=True, methods=['post'], url_path='bayar')
    @transaction.atomic
    def bayar(self, request, pk=None):
        """
        Menandai tagihan sebagai lunas untuk bulan ini.
        Secara otomatis akan membuat record Transaksi dan mengurangi saldo Rekening.
        URL: POST /api/status-tagihan/{id}/bayar/
        """
        tagihan = self.get_object()
        today = datetime.date.today()
        bulan, tahun = today.month, today.year

        status_tagihan, created = StatusTagihan.objects.get_or_create(
            tagihan=tagihan,
            bulan=bulan,
            tahun=tahun
        )

        if status_tagihan.status_lunas:
            return Response(
                {'error': 'Tagihan ini sudah ditandai lunas.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rekening_terkait = Rekening.objects.select_for_update().get(pk=tagihan.rekening.pk)
        rekening_terkait.saldo -= tagihan.jumlah_tagihan
        rekening_terkait.save()
        
        transaksi_baru = Transaksi.objects.create(
            user=request.user,
            rekening=tagihan.rekening,
            kategori=tagihan.kategori,
            deskripsi=tagihan.deskripsi,
            jumlah=tagihan.jumlah_tagihan,
            jenis=Transaksi.Jenis.PENGELUARAN,
            tanggal=today
        )

        status_tagihan.status_lunas = True
        status_tagihan.transaksi_pembayaran = transaksi_baru
        status_tagihan.save()

        return Response(
            {'status': 'success', 'message': f"'{tagihan.deskripsi}' telah ditandai lunas."},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='notifikasi-jatuh-tempo')
    def notifikasi_jatuh_tempo(self, request):
        """
        Mengembalikan daftar tagihan yang akan jatuh tempo dalam 7 hari
        dan belum lunas untuk bulan ini.
        URL: GET /api/status-tagihan/notifikasi-jatuh-tempo/
        """
        user = request.user
        today = timezone.localdate()

        seven_days_later = today + timedelta(days=7)
        
        tagihan_aktif = Tagihan.objects.filter(user=user, aktif=True)
        
        notifikasi_list = []
        
        for tagihan in tagihan_aktif:
            try:
                due_date_this_month = today.replace(day=tagihan.hari_jatuh_tempo)
            except ValueError:
                continue

            if today <= due_date_this_month <= seven_days_later:
                status_obj, created = StatusTagihan.objects.get_or_create(
                    tagihan=tagihan,
                    bulan=today.month,
                    tahun=today.year
                )
                if not status_obj.status_lunas:
                    notifikasi_list.append(tagihan)

        serializer = self.get_serializer(notifikasi_list, many=True)
        return Response(serializer.data)