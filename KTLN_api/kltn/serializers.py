from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *
from rest_framework import serializers
from django.db.models import Avg, Sum


class KhoaSerializer(ModelSerializer):
    class Meta:
        model = Khoa
        fields = '__all__'


class ItemSerializer(ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['avt'] = instance.avt.url

        return req


class UserInfoSerializer(ItemSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'chucvu', 'avt']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ThanhVienHoiDongSerializer(ModelSerializer):
    class Meta:
        model = ThanhVien_HoiDong
        fields = ['vaitro']


class TieuChiSerializer(ModelSerializer):
    class Meta:
        model = TieuChi
        fields = ['ten']


class ThanhVienHoiDongDetailSerializer(ModelSerializer):
    class Meta:
        model = ThanhVien_HoiDong
        fields = ['id', 'vaitro']


class HoiDongSerializer(ModelSerializer):
    thanhviens = ThanhVienHoiDongSerializer(source='thanhvien_hoidong_set', many=True, read_only=True)
    trangthai = SerializerMethodField()

    class Meta:
        model = HoiDong
        fields = ['id', 'ten', 'trangthai', 'thanhviens']

    def get_trangthai(self, obj):
        if obj.thanhviens.count() >= 3:
            trangthai = True
        else:
            trangthai = False
        return trangthai


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avt', 'chucvu']
        extra_kwargs = {
            'password': {
                'write_only': 'true'
            }
        }


class KhoaLuanInfoSerializer(ModelSerializer):
    class Meta:
        model = KhoaLuan
        fields = ['ten']


class ChiTietDiemSerializer(ModelSerializer):
    tieuchi = serializers.CharField()

    class Meta:
        model = KhoaLuan_TieuChi
        fields = ['tieuchi', 'so_diem', 'nhanxet', 'nguoi_danhgia']

    def get_tieuchi(self, obj):
        return obj.tieuchi.ten


class DiemSerializer(ModelSerializer):
    diems = ChiTietDiemSerializer(many=True, source='khoaluan_tieuchi_set')
    ten = serializers.CharField(read_only=True)
    total_score = serializers.SerializerMethodField()

    class Meta:
        model = KhoaLuan
        fields = ['ten', 'total_score', 'diems']

    def get_total_score(self, obj):
        total_score = obj.khoaluan_tieuchi_set.aggregate(sum_score=Avg('so_diem')).get('sum_score')
        return total_score
