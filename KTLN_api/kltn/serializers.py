from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *
from rest_framework import serializers


class UserInfoSerializer(ModelSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = User
        fields = ['full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ThanhVienHoiDongSerializer(ModelSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = ThanhVien_HoiDong
        fields = ['id','vaitro', 'thanhvien', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.thanhvien.first_name} {obj.thanhvien.last_name}"

class KhoaSerializer(ModelSerializer):
    class Meta:
        model = Khoa
        fields = '__all__'


class HoiDongSerializer(ModelSerializer):
    thanhviens = ThanhVienHoiDongSerializer(source='thanhvien_hoidong_set',many=True)

    class Meta:
        model = HoiDong
        fields = ['id', 'ten', 'thanhviens']

