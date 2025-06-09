from django.db import models
from django.contrib.auth.models import User

class Rekening(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rekening')
    nama_bank = models.CharField(max_length=100)
    no_rekening = models.CharField(max_length=50, blank=True, null=True)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    class Meta:
        verbose_name_plural = "Rekening"
        unique_together = ('user', 'nama_bank', 'no_rekening') # Mencegah duplikat

    def __str__(self):
        return f"{self.nama_bank} - (Saldo: {self.saldo})"