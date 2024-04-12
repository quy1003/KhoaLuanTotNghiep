from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *
from rest_framework import serializers

class ItemSerializer(ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['avt'] = instance.avt.url

        return req

class UserInfoSerializer(ItemSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = User
        fields = ['username','full_name','email', 'chucvu', 'avt']

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
    trangthai = SerializerMethodField()

    class Meta:
        model = HoiDong
        fields = ['id', 'ten', 'trangthai', 'trangthai','thanhviens']

    def get_trangthai(self, obj):
        if obj.thanhviens.count() >=3:
            trangthai = True
        else:
            trangthai = False
        return trangthai



