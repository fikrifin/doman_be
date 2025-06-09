from django.db import models
from django.contrib.auth.models import User
from .rekening import Rekening
from .kategori import Kategori

class Transaksi(models.Model):
    class Jenis(models.TextChoices):
        PEMASUKAN = 'IN', 'Pemasukan'
        PENGELUARAN = 'OUT', 'Pengeluaran'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaksi')
    rekening = models.ForeignKey(Rekening, on_delete=models.PROTECT, related_name='transaksi')
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True)
    deskripsi = models.CharField(max_length=255)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2, help_text="Jumlah transaksi dalam Rupiah")
    jenis = models.CharField(max_length=3, choices=Jenis.choices)
    tanggal = models.DateField()
    
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Transaksi'
        app_label = "transaksi"

    def __str__(self):
        return f"{self.deskripsi} - {self.get_jenis_display()} - Rp{self.jumlah}"