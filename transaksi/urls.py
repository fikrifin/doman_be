from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transaksi.views import (
    KategoriViewSet,
    TransaksiViewSet,
    TransaksiWajibViewSet,
    ChecklistWajibViewSet,
)

# Buat router dan daftarkan viewsets kita
router = DefaultRouter()
router.register(r'kategori', KategoriViewSet, basename='kategori')
router.register(r'transaksi', TransaksiViewSet, basename='transaksi')
router.register(r'transaksi-wajib', TransaksiWajibViewSet, basename='transaksi-wajib')
router.register(r'checklist', ChecklistWajibViewSet, basename='checklist')

# URL Patterns API akan ditangani oleh router secara otomatis.
urlpatterns = [
    path('', include(router.urls)),
]