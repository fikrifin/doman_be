from rest_framework import serializers
from transaksi.models.transaksiwajib import TransaksiWajib

class TransaksiWajibSerializer(serializers.ModelSerializer):
    kategori_nama = serializers.CharField(source='kategori.nama', read_only=True)
    
    class Meta:
        model = TransaksiWajib
        fields = [
            'id', 'kategori', 'kategori_nama', 'deskripsi', 
            'jumlah_estimasi', 'hari_jatuh_tempo', 'aktif'
        ]
        extra_kwargs = {'kategori': {'write_only': True}}