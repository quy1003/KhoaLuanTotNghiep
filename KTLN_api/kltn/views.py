from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from rest_framework import generics
from django.db.models import Prefetch

class KhoaViewset(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Khoa.objects.all()
    serializer_class = KhoaSerializer


class HoiDongViewset(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = HoiDong.objects.prefetch_related('thanhviens').all()
    serializer_class = HoiDongSerializer


class ThanhVienHoiDongViewset(viewsets.ModelViewSet, generics.ListAPIView):

    queryset = ThanhVien_HoiDong.objects.all()
    serializer_class = ThanhVienHoiDongSerializer
