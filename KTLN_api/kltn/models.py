from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.contrib.auth.hashers import make_password
import datetime


class User(AbstractUser):
    avt = CloudinaryField()
    phone = models.CharField(max_length=20, null=True, default='999999999')
    diachi = models.CharField(max_length=255, null=True, default='TP HCM')
    ngaysinh = models.DateField(null=True, default='2003-01-01')
    gioitinh = models.BooleanField(null=True)


class SinhVien(User):
    khoaluan = models.ForeignKey('KhoaLuan', on_delete=models.PROTECT, related_name='sinhvien_khoaluan', null=True)
    nganh = models.ForeignKey('Nganh', on_delete=models.CASCADE)
    nienkhoa = models.ForeignKey('NienKhoa', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Băm mật khẩu trước khi lưu vào cơ sở dữ liệu
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class GiaoVu(User):
    chucvu = models.CharField(max_length=100, null=False)

    class Meta:
        verbose_name_plural = 'Giao Vu'
        verbose_name = 'Giao Vu'

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Khoa(models.Model):
    ten_khoa = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        verbose_name_plural = 'Khoa'
        verbose_name = 'Khoa'

    def __str__(self):
        return self.ten_khoa


class Nganh(models.Model):
    ten_nganh = models.CharField(max_length=100, unique=True, null=False)
    khoa = models.ForeignKey(Khoa, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Nganh'
        verbose_name = 'Nganh'

    def __str__(self):
        return self.ten_nganh


class NienKhoa(models.Model):
    nam_batdau = models.DateField()
    nam_ketthuc = models.DateField()

    def __str__(self):
        return str(self.nam_batdau)

    class Meta:
        verbose_name_plural = 'Nien Khoa'
        verbose_name = 'Nien Khoa'


class GiangVien(User):
    hocham = models.CharField(max_length=30)
    khoa = models.ForeignKey(Khoa, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Giang Vien'
        verbose_name = 'Giang Vien'

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class HoiDong(models.Model):
    chutich = models.ForeignKey(GiangVien, on_delete=models.CASCADE, related_name='hoidong_chutichvien')
    thuky = models.ForeignKey(GiangVien, on_delete=models.CASCADE, related_name='hoidong_thuky')
    phanbien = models.ForeignKey(GiangVien, on_delete=models.CASCADE, related_name='hoidong_phanbien')
    giangvien = models.ManyToManyField(GiangVien, related_name='hoidong_giangvien')

    class Meta:
        verbose_name_plural = 'Hoi Dong'
        verbose_name = 'Hoi Dong'


class TieuChi(models.Model):
    ten_tieuchi = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        verbose_name_plural = 'Tieu Chi'
        verbose_name = 'Tieu Chi'

    def __str__(self):
        return self.ten_tieuchi


class KhoaLuan(models.Model):
    giaovu = models.ForeignKey(GiaoVu, on_delete=models.PROTECT)
    ten_khoaluan = models.CharField(max_length=200)
    mo_ta = models.TextField(null=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_capnhat = models.DateTimeField(auto_now=True)
    hoidong = models.ForeignKey(HoiDong, on_delete=models.PROTECT, related_name='khoaluan_hoidong', null=True)
    giangvien = models.ManyToManyField(GiangVien, related_name='khoaluan_giangvien')
    nienkhoa = models.ForeignKey(NienKhoa, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Khoa Luan'
        verbose_name = 'Khoa Luan'

    def __str__(self):
        return self.ten_khoaluan


class Diem(models.Model):
    giangvien = models.ForeignKey(GiangVien, on_delete=models.CASCADE)
    tieuchi = models.ForeignKey(TieuChi, on_delete=models.CASCADE)
    khoaluan = models.ForeignKey(KhoaLuan, on_delete=models.CASCADE)
    sodiem = models.IntegerField()
    nhanxet = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Diem'
        verbose_name = 'Diem'
