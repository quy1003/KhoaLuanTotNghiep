from rest_framework.serializers import ModelSerializer
from .models import SinhVien,GiangVien,GiaoVu,HoiDong,Hoidong_Giangvien,KhoaLuan

class SinhVienSerializer(ModelSerializer):
    class Meta:
        model = SinhVien
        fields = "__all__"

class GiangVienSerializer(ModelSerializer):
    class Meta:
        model = GiangVien
        fields = "__all__"
class GiaoVuSerializer(ModelSerializer):
    class Meta:
        model = GiaoVu
        fields = "__all__"
class KhoaLuanSerializer(ModelSerializer):
    class Meta:
        model = KhoaLuan
        fields = "__all__"