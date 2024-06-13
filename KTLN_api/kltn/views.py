from django.shortcuts import render
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status, parsers
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action
from kltn import serializers
from .models import *
from .serializers import *
from rest_framework import generics
from django.db.models import Prefetch
from kltn.perms import IsPermitUser, IsPermitUserGivePoint, IsPermitMinistry
from . import paginators
from django.shortcuts import render
class KhoaViewset(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = Khoa.objects.all()
    serializer_class = KhoaSerializer


class Khoa_KhoaLuanViewset(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Khoa.objects.all()
    serializer_class = KhoaSerializer

    @action(methods=['get'], url_path='khoaluans', detail=True)
    def get_khoaluans(self, request, pk):
        khoa = self.get_object()
        khoaluans = KhoaLuan.objects.filter(khoa=khoa)
        q = request.query_params.get('q')
        if q:
            khoaluans = khoaluans.filter(ten__icontains=q)

        serializer = KhoaLuanInfoSerializer(khoaluans, many=True)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class HoiDongViewset(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    queryset = HoiDong.objects.prefetch_related('thanhviens').all()
    serializer_class = HoiDongSerializer
    permission_classes = [permissions.AllowAny]


    def get_queryset(self):
        queryset = self.queryset
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(ten__icontains=q)
            return queryset
        queryset = queryset.prefetch_related('thanhviens')
        return queryset


class HoiDongDetailViewset(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = HoiDong.objects.prefetch_related('thanhviens').all()
    serializer_class = HoiDongSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(ten__icontains=q)

        return queryset

    @action(methods=['get'], url_path='thanhviens', detail=True)
    def get_thanhviens(self, request, pk):
        hoidong = self.get_object()
        thanhviens = hoidong.thanhviens.all()

        serializer = UserInfoWithRoleSerializer(thanhviens, many=True,context={'hoidong_id': hoidong.id})
        print(hoidong.id)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


    @action(methods=['delete'], url_path='thanhviens/delete/(?P<thanhvien_id>\d+)', detail=True)
    def destroy_thanhvien(self, request, pk, thanhvien_id):
        hoidong = self.get_object()
        thanhvien = ThanhVien_HoiDong.objects.get(thanhvien_id=thanhvien_id, hoidong_id=hoidong)
        try:

            thanhvien.delete()
            return Response({'msg:': 'Xoa Thanh Cong'}, status=status.HTTP_200_OK)
        except thanhvien.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], url_path='thanhviens/create', detail=True)
    def post_thanhvien(self, request, pk):
        hoidong = self.get_object()
        thanhvien_id = request.data.get('thanhvien_id')
        vaitro = request.data.get('vaitro')


        if hoidong.thanhviens.filter(thanhvien_hoidong__vaitro='THANH VIEN KHAC').count()==2 and vaitro.__eq__("THANH VIEN KHAC") :
            return Response({'error:':'Hoi Dong Co Toi Da 2 chuc vu nay'}, status=status.HTTP_400_BAD_REQUEST)
        if hoidong.thanhviens.count() == 5:
            return Response({'error:', 'So Thanh Vien Da Dat Toi Toi Da'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            thanhvien = User.objects.get(id=thanhvien_id)
        except User.DoesNotExist:
            return Response({'error:': 'Thanh vien khong ton tai'}, status=status.HTTP_404_NOT_FOUND)
        if vaitro not in [choice[0] for choice in ThanhVien_HoiDong.roles]:
            return Response({'error: ': 'Vai tro khong hop le'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if vaitro != 'THANH VIEN KHAC':
                if ThanhVien_HoiDong.objects.filter(hoidong=hoidong, vaitro=vaitro).exists():
                    return Response({'error:': 'Hoi Dong Nay Da Co Chuc Vu Nay'}, status=status.HTTP_400_BAD_REQUEST)

        if ThanhVien_HoiDong.objects.filter(thanhvien=thanhvien, hoidong=hoidong).exists():
            return Response({'error:': 'Thanh vien da co trong hoi dong'}, status=status.HTTP_400_BAD_REQUEST)

        thanhvien_hoidong = ThanhVien_HoiDong(thanhvien=thanhvien, hoidong=hoidong, vaitro=vaitro)
        thanhvien_hoidong.save()

        serializer = ThanhVienHoiDongSerializer(thanhvien_hoidong)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    ###
    @action(methods=['patch'], url_path='thanhviens/patch', detail=True)
    def patch_thanhvien(self, request, pk):
        hoidong = self.get_object()
        thanhvien_id = request.data.get('thanhvien_id')
        vaitro = request.data.get('vaitro')


        try:
            thanhvien = User.objects.get(pk=thanhvien_id)
        except User.DoesNotExist:
            return Response({'error:': 'Thanh vien khong ton tai'}, status=status.HTTP_404_NOT_FOUND)
        if hoidong.thanhviens.filter(thanhvien_hoidong__vaitro='THANH VIEN KHAC').count()==2 and vaitro.__eq__("THANH VIEN KHAC") :
            return Response({'error:':'Hoi Dong Co Toi Da 2 chuc vu nay'}, status=status.HTTP_400_BAD_REQUEST)
        if vaitro not in [choice[0] for choice in ThanhVien_HoiDong.roles]:
            return Response({'error: ': 'Vai tro khong hop le'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if vaitro != 'THANH VIEN KHAC':
                if ThanhVien_HoiDong.objects.filter(hoidong=hoidong, vaitro=vaitro).exists():
                    return Response({'error:': 'Hoi Dong Nay Da Co Chuc Vu Nay'}, status=status.HTTP_400_BAD_REQUEST)
        thanhvien_hoidong = ThanhVien_HoiDong.objects.get(thanhvien=thanhvien, hoidong=hoidong)
        thanhvien_hoidong.vaitro = vaitro
        thanhvien_hoidong.save()

        serializer = ThanhVienHoiDongSerializer(thanhvien_hoidong)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    ###
    def get_permissions(self):
        if self.action in ['destroy_thanhvien', 'post_thanhvien', 'patch_thanhvien']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


class ThanhVienHoiDongViewset(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = ThanhVien_HoiDong.objects.all()
    serializer_class = ThanhVienHoiDongDetailSerializer


class UserTestViewset(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

class UserViewset(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_name='current-user', detail=False)
    def current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(UserSerializer(user).data)

    @action(methods=['get'], url_path='current_user/my_hoidong', detail=False)
    def my_hoidong(self, request):
        user = self.request.user
        thanhvien_hoidong = ThanhVien_HoiDong.objects.filter(thanhvien=user)
        serializer = ThanhVien_HoiDongSerializer(thanhvien_hoidong, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class DiemViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = KhoaLuan.objects.prefetch_related('tieuchis').all()
    serializer_class = DiemSerializer


class DiemDetailViewset(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = KhoaLuan.objects.all()
    serializer_class = DiemSerializer
    permission_classes = [permissions.AllowAny]

    # def get_permissions(self):
    #     if self.action in ['post_diem']:
    #         return [permissions.IsAuthenticated(), IsPermitUserGivePoint()]
    #     return self.permission_classes

    @action(methods=['post'], url_path='create', detail=True)
    def post_diem(self, request, pk):
        khoaluan = self.get_object()
        try:
            tieuchi = TieuChi.objects.get(ten=request.data.get('tieuchi'))
        except:
            return Response({'ERROR:': 'Tieu chi phai thuoc nhom cac tieu chi'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_superuser != 1 and not khoaluan.hoidong.thanhviens.filter(id=request.user.id).exists() :
            return Response({'ERROR:':'Nguoi danh gia phai thuoc hoi dong'}, status=status.HTTP_400_BAD_REQUEST)

        if khoaluan.tieuchis.filter(ten=tieuchi).exists():
            return Response({'ERROR: ': 'Khoa Luan Nay Da Co Diem Tieu Chi Nay'}, status=status.HTTP_400_BAD_REQUEST)
        diem = KhoaLuan_TieuChi.objects.create(nguoi_danhgia=request.user,
                                               nhanxet=request.data.get('nhanxet'),
                                               tieuchi=tieuchi,
                                               so_diem=request.data.get('so_diem'),
                                               khoaluan=self.get_object())
        diem.save()
        return Response(ChiTietDiemSerializer(diem).data, status=status.HTTP_201_CREATED)

class ListKhoaLuanViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = KhoaLuan.objects.all()
    serializer_class = KhoaLuanInfoSerializer
    pagination_class = paginators.Paginator

class KhoaLuanViewset(viewsets.ViewSet,generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = KhoaLuan.objects.all()
    serializer_class = KhoaLuanSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]
    pagination_class = paginators.Paginator

    def get_queryset(self):
        queryset = self.queryset
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(ten__icontains=q)
            return queryset
        queryset = queryset.prefetch_related('gv_huongdan')
        queryset = queryset.prefetch_related('sinhvien')
        queryset = queryset.prefetch_related('tieuchis')
        return queryset

    def list_khoaluan(self, request):
        queryset = self.get_queryset()
        serializer = KhoaLuanInfoSerializer(queryset, many=True)
        return Response(serializer.data)
    #
    @action(methods=['get'], url_path='diem_detail', detail=True)
    def diem_detail(self, reqest, pk):
        khoaluan = self.get_object()
        return Response(DiemSerializer(khoaluan).data)


    @action(methods=['patch'], url_path='update_link', detail=True)
    def update_link(self, request, pk):
        khoaluan = self.get_object()
        khoaluan.link = request.data.get('link')
        khoaluan.save()
        serializer = KhoaLuanSerializer(khoaluan)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(methods=['patch'], url_path='block', detail=True)
    def block_khoaluan(self, request, pk):
        khoaluan = self.get_object()
        khoaluan.trangthai = not khoaluan.trangthai
        khoaluan.save()
        serializer = KhoaLuanSerializer(khoaluan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(methods=['get'], url_path='get_tieuchi_not', detail=True)
    def get_tieuchi_not(self, request, pk):
        khoaluan = self.get_object()
        tieuchis = khoaluan.tieuchis.all()
        tieuchis_chuaco = TieuChi.objects.exclude(id__in=tieuchis.values_list('id', flat=True))
        serializer = TieuChiNotIn(tieuchis_chuaco, many=True)
        print(tieuchis_chuaco)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(methods=['post'], url_path='create_diem', detail=True)
    def create_diem(self, request,pk):
        khoaluan = self.get_object()
        try:
            tieuchi = TieuChi.objects.get(ten=request.data.get('tieuchi'))
        except:
            return Response({'ERROR:': 'Tieu chi phai thuoc nhom cac tieu chi'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_superuser != 1 and not khoaluan.hoidong.thanhviens.filter(id=request.user.id).exists() :
            return Response({'ERROR:':'Nguoi danh gia phai thuoc hoi dong'}, status=status.HTTP_400_BAD_REQUEST)

        if khoaluan.tieuchis.filter(ten=tieuchi).exists():
            return Response({'ERROR: ': 'Khoa Luan Nay Da Co Diem Tieu Chi Nay'}, status=status.HTTP_400_BAD_REQUEST)
        diem = KhoaLuan_TieuChi.objects.create(nguoi_danhgia=request.user,
                                               nhanxet=request.data.get('nhanxet'),
                                               tieuchi=tieuchi,
                                               so_diem=request.data.get('so_diem'),
                                               khoaluan=self.get_object())
        diem.save()
        return Response(ChiTietDiemSerializer(diem).data, status=status.HTTP_201_CREATED)
    ##
    @action(methods=['post'], url_path='create-khoaluan', detail=False)
    def create_khoaluan(self, request):
        ten = request.data.get('ten')
        ghichu = request.data.get('ghichu')
        giaovu_id = request.user
        hoidong_id = request.data.get('hoidong_id')
        khoa_id = request.data.get('khoa')
        sinhvien_id = request.data.get('sinhvien', [])
        gvhuongdan_id = request.data.get('gv_huongdan', [])
        sinhvien = User.objects.filter(pk__in=sinhvien_id, chucvu='HOCSINH')
        if len(sinhvien) != len(sinhvien_id):
            return Response({'err: ': 'Vui lòng chỉ nhập ID của người dùng có chức vụ HOCSINH'}, status=status.HTTP_400_BAD_REQUEST)

        gvhd = User.objects.filter(pk__in=gvhuongdan_id, chucvu='GIANGVIEN')
        if len(gvhd) != len(gvhuongdan_id):
            return Response({'err: ': 'Vui lòng chỉ nhập ID của người dùng có chức vụ GIANGVIEN'}, status=status.HTTP_400_BAD_REQUEST)

        if not (ten and khoa_id):
            return Response({'error': 'ten and khoa_id là bắt buộc'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            giaovu = request.user
            khoa = Khoa.objects.get(pk=khoa_id)
            hoidong = HoiDong.objects.get(pk=hoidong_id)
            sinhvien = User.objects.filter(pk__in=sinhvien_id)
            gv_huongdan = User.objects.filter(pk__in=gvhuongdan_id)
            # tieuchi = TieuChi.objects.filter(pk__in=tieuchi_id)

            new_khoaluan = KhoaLuan.objects.create(
                ten=ten, ghichu=ghichu, hoidong=hoidong,giaovu=request.user, khoa=khoa)

            new_khoaluan.sinhvien.set(sinhvien)
            new_khoaluan.gv_huongdan.set(gv_huongdan)
            # new_khoaluan.tieuchi.set(tieuchi)

            data = KhoaLuanSerializer(new_khoaluan).data
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], url_path='update-khoaluan', detail=True)
    def update_khoaluan(self, request, pk):
        khoaluan = self.get_object()
        fields_to_update = ['ten', 'link',
                            'ghichu', 'sinhvien', 'gv_huongdan', 'trangthai', 'giaovu','khoa', 'hoidong_id']  # cac truong dduoc phep update

        try:
            for field in fields_to_update:
                if field in request.data:


                    ###
                    #if field == 'khoa'
                    # try:
                    #         khoaluan.khoa = Khoa.objects.get(request.data.get('khoa'))
                    #     except Exception as e:
                    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                    ###
                    if field == 'hoidong_id':
                        hoidong_id = request.data['hoidong_id']
                        try:

                            hoidong = HoiDong.objects.get(pk=hoidong_id)
                            khoaluan.hoidong = hoidong
                            khoaluan.save()
                        except Exception as e:
                            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                    if field != 'khoa':
                        data = request.data[field]
                        if isinstance(data, list):
                            users = User.objects.filter(pk__in=data)
                            getattr(khoaluan, field).set(users)
                        else:
                            setattr(khoaluan, field, data)

                    else:
                        khoa_id = request.data['khoa']
                        try:

                            khoa = Khoa.objects.get(pk=khoa_id)
                            khoaluan.khoa = khoa
                            khoaluan.save()
                        except Exception as e:
                            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                elif field != 'sinhvien':  # Kiểm tra nếu trường không phải là 'sinhvien'
                    continue  # Bỏ qua việc cập nhật trường này nếu không có trong request.data

            khoaluan.save()
            data = KhoaLuanSerializer(khoaluan).data
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['delete'], url_path='delete-KhoaLuan')
    def delete_khoaluan(self, request, pk=None):
        try:
            khoaluan = self.get_object()
            khoaluan.delete()
            return Response({'message': 'KhoaLuan đã được xóa thành công'}, status=status.HTTP_204_NO_CONTENT)
        except KhoaLuan.DoesNotExist:
            return Response({'error': 'KhoaLuan không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, url_path="not-hoidong")
    def not_hoidong(self, request):
        filtered_khoaluan = KhoaLuan.objects.filter(trangthai=True, hoidong__isnull=True)
        serialized_KhoaLuan = KhoaLuanSerializer(filtered_khoaluan, many=True).data
        return Response(serialized_KhoaLuan, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path="my-khoaluan")
    def my_khoaluan(self, request):
        user = request.user
        mykhoaluan = KhoaLuan.objects.filter(Q(sinhvien=user) | Q(gv_huongdan=user) | Q(hoidong__thanhviens=user)).distinct()
        if mykhoaluan.exists():
            data = KhoaLuanSerializer(mykhoaluan, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message": "Không có khóa luận nào!!!"}, status=status.HTTP_404_NOT_FOUND)

    # def get_permissions(self):
    #     if self.action in ['delete_khoaluan', 'update_khoaluan', 'create_khoaluan', 'create_diem']:
    #         return [permissions.IsAuthenticated()]
    #     return super().get_permissions()

class TieuChiViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = TieuChi.objects.all();
    serializer_class = TieuChiSerializer


class EmailViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.all();
    serializer_class = EmailSerializer

class UserInfoViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.all();
    serializer_class = UserNameAndId
    def get_permissions(self):
        # if self.action in ['destroy_thanhvien', 'post_thanhvien', 'patch_thanhvien']:
        return [permissions.IsAuthenticated()]


####
def home(request):
    return render(request, 'home.html', {
        'message': 'Hello, World!'
    })

def diem_detail(request, id):
    return render(request, 'diem_detail.html', {'id': id})
