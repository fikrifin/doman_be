from django.contrib import admin
from .models import Rekening, Kategori, Transaksi, Tagihan, StatusTagihan

# Register your models here.
admin.site.register(Rekening)
admin.site.register(Kategori)
admin.site.register(Transaksi)
admin.site.register(Tagihan)
admin.site.register(StatusTagihan)