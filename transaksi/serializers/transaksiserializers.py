from rest_framework import serializers
from transaksi.models.transaksi import Transaksi

class TransaksiSerializer(serializers.ModelSerializer):
    rekening_info = serializers.CharField(source='rekening.__str__', read_only=True)
    kategori_nama = serializers.CharField(source='kategori.nama', read_only=True)

    class Meta:
        model = Transaksi
        fields = [
            'id', 'rekening', 'rekening_info', 'kategori', 'kategori_nama', 
            'deskripsi', 'jumlah', 'jenis', 'tanggal'
        ]

        extra_kwargs = {
            'rekening': {'write_only': True},
            'kategori': {'write_only': True}
        }