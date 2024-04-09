from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions
from .models import SinhVien, GiangVien
from .serializers import SinhVienSerializer,GiangVienSerializer,GiaoVuSerializer,KhoaLuanSerializer

class SinhVienViewset(viewsets.ModelViewSet):
    queryset = SinhVien.objects.filter(is_active = True)
    serializer_class = SinhVienSerializer
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class GiangVienViewset(viewsets.ModelViewSet):
    queryset = GiangVien.objects.filter(is_active = True)
    serializer_class = GiangVienSerializer
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
