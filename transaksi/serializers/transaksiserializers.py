from rest_framework import serializers
from transaksi.models.transaksi import Transaksi

class TransaksiSerializer(serializers.ModelSerializer):
    # Tampilkan nama kategori, bukan hanya ID-nya
    kategori_nama = serializers.CharField(source='kategori.nama', read_only=True)

    class Meta:
        model = Transaksi
        fields = [
            'id', 'kategori', 'kategori_nama', 'deskripsi', 
            'jumlah', 'jenis', 'tanggal', 'dibuat_pada'
        ]
        # kategori adalah write-only, karena kita akan menampilkannya sebagai kategori_nama
        extra_kwargs = {'kategori': {'write_only': True}}