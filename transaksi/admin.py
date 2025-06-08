from django.contrib import admin
from .models import Kategori, Transaksi, TransaksiWajib, StatusPembayaranWajib

# Register your models here.
admin.site.register(Kategori)
admin.site.register(Transaksi)
admin.site.register(TransaksiWajib)
admin.site.register(StatusPembayaranWajib)