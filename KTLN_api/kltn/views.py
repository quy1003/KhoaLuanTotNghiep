# from django.shortcuts import render
# from django.views import View
# from rest_framework import viewsets, permissions
# from .models import SinhVien, GiangVien, TieuChi
# from .serializers import SinhVienSerializer,GiangVienSerializer,GiaoVuSerializer,KhoaLuanSerializer, TieuChiSerializer
# from rest_framework import generics
#
# class SinhVienViewset(viewsets.ModelViewSet):
#     queryset = SinhVien.objects.filter(is_active = True)
#     serializer_class = SinhVienSerializer
#     def get_permissions(self):
#         if self.action == 'list':
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]
#
# class GiangVienViewset(viewsets.ModelViewSet):
#     queryset = GiangVien.objects.filter(is_active = True)
#     serializer_class = GiangVienSerializer
#     def get_permissions(self):
#         if self.action == 'list':
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]
#
#
# class TieuChiViewset(viewsets.ViewSet, generics.ListAPIView):
#     queryset = TieuChi.objects.all()
#     serializer_class = TieuChiSerializer
