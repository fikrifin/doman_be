from rest_framework import serializers
from transaksi.models.kategori import Kategori

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = ['id', 'nama']