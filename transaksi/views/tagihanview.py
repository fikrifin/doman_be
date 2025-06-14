import datetime
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from transaksi.models.tagihan import Tagihan
from transaksi.serializers.tagihanserializers import TagihanSerializer

class TagihanViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk CRUD template Transaksi Wajib.
    """
    serializer_class = TagihanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Tagihan.objects.filter(user=self.request.user).order_by('-aktif')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)