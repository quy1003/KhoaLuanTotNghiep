from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action
from kltn import serializers
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

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(ten__icontains=q)

        return  queryset

    @action(methods=['get'], url_path='thanhviens', detail=True)
    def get_thanhviens(self, request, pk):
        hoidong = self.get_object()
        thanhviens = hoidong.thanhviens.all()
        q = request.query_params.get('q')
        if q:
            thanhviens = thanhviens.filter(Q(username__icontains=q) |
                                           Q(first_name__icontains=q) |
                                           Q(last_name__icontains=q))

        serializer = UserInfoSerializer(thanhviens, many=True)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)



class ThanhVienHoiDongViewset(viewsets.ModelViewSet, generics.ListAPIView):

    queryset = ThanhVien_HoiDong.objects.all()
    serializer_class = ThanhVienHoiDongSerializer

