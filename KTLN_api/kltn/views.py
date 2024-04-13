from django.shortcuts import render
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action
from kltn import serializers
from .models import *
from .serializers import *
from rest_framework import generics
from django.db.models import Prefetch
from kltn.perms import IsPermitUser
class KhoaViewset(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = Khoa.objects.all()
    serializer_class = KhoaSerializer


class HoiDongViewset(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = HoiDong.objects.prefetch_related('thanhviens').all()
    serializer_class = HoiDongSerializer
    permission_classes = [permissions.AllowAny]
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

    @action(methods=['delete'], url_path='thanhviens/delete/(?P<thanhvien_id>\d+)', detail=True)
    def destroy_thanhvien(self,request, pk, thanhvien_id):
        hoidong = self.get_object()
        try:
            thanhvien = ThanhVien_HoiDong.objects.get(thanhvien_id=thanhvien_id, hoidong_id=hoidong)
            thanhvien.delete()
            return Response({'msg:':'Xoa Thanh Cong'},status=status.HTTP_204_NO_CONTENT)
        except ThanhVien_HoiDong.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], url_path='thanhviens/create', detail=True)
    def post_thanhvien(self, request, pk):
        hoidong = self.get_object()
        thanhvien_id = request.data.get('thanhvien_id')
        vaitro = request.data.get('vaitro')
        if hoidong.thanhviens.count() == 5:
            return Response({'error:','So Thanh Vien Da Dat Toi Toi Da'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            thanhvien = User.objects.get(id=thanhvien_id)
        except User.DoesNotExist:
            return Response({'error:':'Thanh vien khong ton tai'}, status=status.HTTP_404_NOT_FOUND)
        if vaitro not in [choice[0] for choice in ThanhVien_HoiDong.roles]:
            return Response({'error: ':'Vai tro khong hop le'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if vaitro != 'THANH VIEN KHAC':
                if ThanhVien_HoiDong.objects.filter(hoidong=hoidong, vaitro=vaitro).exists():
                    return Response({'error:':'Hoi Dong Nay Da Co Chuc Vu Nay'}, status=status.HTTP_400_BAD_REQUEST)

        if ThanhVien_HoiDong.objects.filter(thanhvien=thanhvien, hoidong=hoidong).exists():
            return Response({'error:':'Thanh vien da co trong hoi dong'}, status=status.HTTP_400_BAD_REQUEST)

        thanhvien_hoidong = ThanhVien_HoiDong(thanhvien=thanhvien, hoidong=hoidong, vaitro=vaitro)
        thanhvien_hoidong.save()

        serializer = ThanhVienHoiDongSerializer(thanhvien_hoidong)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_permissions(self):
        if self.action in ['destroy_thanhvien', 'post_thanhvien']:
            return [permissions.IsAuthenticated(), IsPermitUser()]
        return super().get_permissions()

class ThanhVienHoiDongViewset(viewsets.ModelViewSet, generics.ListAPIView):

    queryset = ThanhVien_HoiDong.objects.all()
    serializer_class = ThanhVienHoiDongDetailSerializer

