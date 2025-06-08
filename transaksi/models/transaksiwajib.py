from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from .kategori import Kategori

class TransaksiWajib(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaksi_wajib')
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True)
    deskripsi = models.CharField(max_length=255)
    jumlah_estimasi = models.DecimalField(max_digits=12, decimal_places=2, help_text="Estimasi jumlah pengeluaran")
    hari_jatuh_tempo = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        help_text="Tanggal jatuh tempo setiap bulan (1-31)"
    )
    aktif = models.BooleanField(default=True, help_text="Nonaktifkan jika tidak lagi menjadi transaksi wajib")

    class Meta:
        verbose_name_plural = "Transaksi Wajib"
        app_label = "transaksi"

    def __str__(self):
        return f"Wajib: {self.deskripsi} (Jatuh tempo tgl {self.hari_jatuh_tempo})"