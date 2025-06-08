from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer

# Buat router dan daftarkan viewsets kita
router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

# URL Patterns API akan ditangani oleh router secara otomatis.
urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='custom_register'),
    path('', include(router.urls)),
]