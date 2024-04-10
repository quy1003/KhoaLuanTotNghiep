from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.contrib.auth.hashers import make_password
import datetime


class User(AbstractUser):
    roles = (
        ('HOCSINH', 'hocsinh'),
        ('GIANGVIEN', 'giangvien'),
        ('GIAOVU', 'giaovu'),
        ('ADMIN', 'admin')
    )
    chucvu = models.CharField(max_length=50, null=False, choices=roles)
    avt = CloudinaryField(null=True)

    class Meta:
        verbose_name_plural = 'User'
        verbose_name = 'User'

    def __str__(self):
        return self.get_full_name()


class HoiDong(models.Model):
    ten = models.CharField(max_length=100, null=True)
    thanhviens = models.ManyToManyField(User
                                       ,related_name='dsthanhvien',
                                       through='ThanhVien_HoiDong')

    class Meta:
        verbose_name_plural = 'Hoi Dong'
        verbose_name = 'Hoi Dong'

    def __str__(self):
        return self.ten


class ThanhVien_HoiDong(models.Model):
    roles = (
        ('TRUONG BAN', 'truong ban'),
        ('THU KY', 'thu ky'),
        ('PHO BAN', 'pho ban'),
        ('PHAN BIEN', 'phan bien')
    )
    thanhvien = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'chucvu': 'giangvien'})
    hoidong = models.ForeignKey(HoiDong, on_delete=models.CASCADE)
    chucvu = models.CharField(choices=roles, null=False, max_length=100)

    class Meta:
        unique_together = ['thanhvien', 'hoidong']
        verbose_name_plural = 'Thanh Vien - Hoi Dong'
        verbose_name = 'Thanh Vien - Hoi Dong'


class Khoa(models.Model):
    # ds_khoa = (
    #     ('IT', 'Cong Nghe Thong Tin'),
    #     ('AU', 'Ke Kiem'),
    #     ('BT', 'Cong Nghe Sinh Hoc'),
    #     ('FB', 'Tai Chinh Ngan Hang'),
    #     ('AS', 'Dao Tao Dac Biet'),
    #     ('BA', 'Quan Tri Kinh Doanh')
    # )
    ten = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Khoa'
        verbose_name = 'Khoa'

    def __str__(self):
        return self.ten


class KhoaLuan(models.Model):
    ten = models.CharField(max_length=200)
    giaovu = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'chucvu':'giaovu'})
    ngaytao = models.DateTimeField(auto_now_add=True)
    ngaycapnhat = models.DateTimeField(auto_now=True)
    link = models.TextField(null=True, blank=True)
    ghichu = models.TextField(blank=True, null=True)
    khoa = models.ForeignKey(Khoa, on_delete=models.CASCADE)
    hoidong = models.ForeignKey(HoiDong, on_delete=models.CASCADE, blank=True, null=True)
    gv_huongdan = models.ManyToManyField(User, related_name='gv_huongdans')
    sinhvien = models.ManyToManyField(User, related_name='sinhviens',limit_choices_to={'chucvu': 'hocsinh'})
    class Meta:
        verbose_name_plural = 'Khoa Luan'
        verbose_name = 'Khoa Luan'

    def __str__(self):
        return self.ten


class TieuChi(models.Model):
    ds_tieuchi = (
        ('HINH THUC', 'hinh thuc'),
        ('PHAN BIEN', 'phan bien'),
        ('THUC HIEN', 'thuc hien'),
        ('DO KHO', 'do kho'),
        ('MO RONG', 'mo rong'),
        ('UNG DUNG', 'ung dung')
    )
    ten = models.CharField(choices=ds_tieuchi, max_length=100)

    class Meta:
        verbose_name_plural = 'Tieu Chi'
        verbose_name = 'Tieu Chi'

    def __str__(self):
        return self.ten


class Diem(models.Model):
    khoaluan = models.ForeignKey(KhoaLuan, on_delete=models.CASCADE)
    tieuchi = models.ManyToManyField(TieuChi, through='Diem_TieuChi',
                                     related_name='tieuchis')

    class Meta:
        verbose_name_plural = 'Diem'
        verbose_name = 'Diem'

    def __str__(self):
        return self.khoaluan.ten


class Diem_TieuChi(models.Model):
    diem = models.ForeignKey(Diem, on_delete=models.CASCADE)
    tieuchi = models.ForeignKey(TieuChi, on_delete=models.CASCADE)
    sodiem = models.FloatField()
    nhanxet = models.TextField(null=True, blank=True)
    nguoi_danhgia = models.ForeignKey(User, on_delete=models.CASCADE,
                                      limit_choices_to={'chucvu':'giangvien'}, null=True)

    class Meta:
        unique_together = ['nguoi_danhgia', 'tieuchi']
        verbose_name_plural = 'Chi Tiet Diem'
        verbose_name = 'Chi Tiet Diem'

    def clean(self):
        super().clean()
        if self.nguoi_danhgia and self.diem.khoaluan.hoidong.thanhviens.all().exists():
            raise ValidationError("Người đánh giá phải thuộc hội đồng.")
