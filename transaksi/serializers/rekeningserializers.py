from rest_framework import serializers
from transaksi.models.rekening import Rekening

class RekeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rekening
        fields = ['id', 'nama_bank', 'no_rekening', 'saldo']
        # Saldo seharusnya tidak bisa diubah langsung melalui API,
        # hanya melalui transaksi.
        read_only_fields = ['saldo']