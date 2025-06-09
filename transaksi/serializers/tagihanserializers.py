from rest_framework import serializers
from transaksi.models.tagihan import Tagihan

class TagihanSerializer(serializers.ModelSerializer):
    kategori_nama = serializers.CharField(source='kategori.nama', read_only=True)
    
    class Meta:
        model = Tagihan
        fields = [
            'id', 'kategori', 'kategori_nama', 'deskripsi', 
            'jumlah_tagihan', 'hari_jatuh_tempo', 'aktif'
        ]
        extra_kwargs = {'kategori': {'write_only': True}}