from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from transaksi.models.rekening import Rekening
from transaksi.serializers.rekeningserializers import RekeningSerializer

class RekeningViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk CRUD Rekening.
    """
    serializer_class = RekeningSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rekening.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)