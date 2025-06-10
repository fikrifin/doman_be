from rest_framework import serializers
from transaksi.models.tagihan import Tagihan

class TagihanSerializer(serializers.ModelSerializer):
    rekening_info = serializers.CharField(source='rekening.__str__', read_only=True)
    
    kategori_nama = serializers.CharField(source='kategori.nama', read_only=True)

    class Meta:
        model = Tagihan
        fields = [
            'id',
            'deskripsi',
            'jumlah_tagihan',
            'hari_jatuh_tempo',
            'aktif',
            'rekening', 
            'rekening_info',
            'kategori', 
            'kategori_nama',
        ]
        extra_kwargs = {
            'rekening': {'write_only': True},
            'kategori': {'write_only': True},
        }
