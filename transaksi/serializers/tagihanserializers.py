from rest_framework import serializers
from transaksi.models.tagihan import Tagihan

class TagihanSerializer(serializers.ModelSerializer):
    # Field read-only untuk menampilkan nama rekening yang mudah dibaca
    rekening_info = serializers.CharField(source='rekening.__str__', read_only=True)
    
    # Field read-only untuk menampilkan nama kategori
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
        # Definisikan field mana yang hanya untuk input
        extra_kwargs = {
            'rekening': {'write_only': True},
            'kategori': {'write_only': True},
        }
