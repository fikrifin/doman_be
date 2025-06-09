from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .transaksi import Transaksi
from .tagihan import Tagihan

class StatusTagihan(models.Model):
    tagihan = models.ForeignKey(Tagihan, on_delete=models.CASCADE, related_name='status_tagihan')
    bulan = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    tahun = models.PositiveIntegerField()
    status_lunas = models.BooleanField(default=False)
    
    # Menghubungkan ke transaksi aktual yang melunasi pembayaran ini
    transaksi_pembayaran = models.OneToOneField(
        Transaksi, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Transaksi yang digunakan untuk melunasi tagihan ini"
    )

    class Meta:
        # Memastikan hanya ada satu entri status untuk setiap transaksi wajib per bulan per tahun
        unique_together = ('tagihan', 'bulan', 'tahun')
        verbose_name_plural = "Status Tagihan"
        app_label = "transaksi"

    def __str__(self):
        status = "Lunas" if self.status_lunas else "Belum Lunas"
        return f"{self.tagihan.deskripsi} ({self.bulan}/{self.tahun}) - {status}"