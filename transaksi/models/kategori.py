from django.db import models
from django.contrib.auth.models import User

class Kategori(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kategori')
    nama = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'nama')
        verbose_name_plural = 'Kategori'
        app_label = "transaksi"

    def __str__(self):
        return self.nama