from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transaksi.views import (
    RekeningViewSet,
    KategoriViewSet,
    TransaksiViewSet,
    TagihanViewSet,
    StatusTagihanViewSet,
)

# Buat router dan daftarkan viewsets kita
router = DefaultRouter()
router.register(r'rekening', RekeningViewSet, basename='rekening')
router.register(r'kategori', KategoriViewSet, basename='kategori')
router.register(r'transaksi', TransaksiViewSet, basename='transaksi')
router.register(r'tagihan', TagihanViewSet, basename='tagihan')
router.register(r'checklist', StatusTagihanViewSet, basename='checklist')

# URL Patterns API akan ditangani oleh router secara otomatis.
urlpatterns = [
    path('', include(router.urls)),
]