import datetime
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Impor semua model yang diperlukan
from transaksi.models.tagihan import Tagihan
from transaksi.models.statustagihan import StatusTagihan
from transaksi.models.rekening import Rekening
from transaksi.models.transaksi import Transaksi

# Impor serializer yang relevan
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
        return Tagihan.objects.filter(user=self.request.user, aktif=True)

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
            # Cari atau buat status untuk bulan ini agar selalu ada di checklist
            status_obj, created = StatusTagihan.objects.get_or_create(
                tagihan=tagihan,
                bulan=bulan,
                tahun=tahun
            )
            
            # Gunakan serializer untuk mendapatkan data dasar dari template Tagihan
            data = self.get_serializer(tagihan).data
            # Tambahkan informasi 'status_lunas' dari objek StatusTagihan
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
        tagihan = self.get_object() # Mengambil instance Tagihan berdasarkan pk dari URL
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

        # 1. Kunci dan perbarui saldo rekening
        # select_for_update() penting untuk mencegah race condition
        rekening_terkait = Rekening.objects.select_for_update().get(pk=tagihan.rekening.pk)
        rekening_terkait.saldo -= tagihan.jumlah_tagihan
        rekening_terkait.save()
        
        # 2. Buat record Transaksi baru, dan pastikan menyertakan rekening
        transaksi_baru = Transaksi.objects.create(
            user=request.user,
            rekening=tagihan.rekening, # <-- INI ADALAH PERBAIKAN UTAMA
            kategori=tagihan.kategori,
            deskripsi=tagihan.deskripsi,
            jumlah=tagihan.jumlah_tagihan,
            jenis=Transaksi.Jenis.PENGELUARAN,
            tanggal=today
        )

        # 3. Perbarui status tagihan
        status_tagihan.status_lunas = True
        status_tagihan.transaksi_pembayaran = transaksi_baru
        status_tagihan.save()

        return Response(
            {'status': 'success', 'message': f"'{tagihan.deskripsi}' telah ditandai lunas."},
            status=status.HTTP_200_OK
        )
