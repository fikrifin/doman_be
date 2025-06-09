from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from .rekening import Rekening
from .kategori import Kategori

class Tagihan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tagihan')
    rekening = models.ForeignKey(Rekening, on_delete=models.CASCADE, related_name='tagihan')
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True)
    deskripsi = models.CharField(max_length=255)
    jumlah_tagihan = models.DecimalField(max_digits=12, decimal_places=2, help_text="Jumlah Tagihan")
    hari_jatuh_tempo = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        help_text="Tanggal jatuh tempo setiap bulan (1-31)"
    )
    aktif = models.BooleanField(default=True, help_text="Nonaktifkan jika tidak lagi menjadi tagihan wajib")

    class Meta:
        verbose_name_plural = "Tagihan"
        app_label = "transaksi"

    def __str__(self):
        return f"Wajib: {self.deskripsi} (Jatuh tempo tgl {self.hari_jatuh_tempo})"