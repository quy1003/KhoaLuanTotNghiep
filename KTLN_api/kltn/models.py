from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
import datetime


class User(AbstractUser):
    avt = CloudinaryField()
    phone = models.CharField(max_length=20, null=False, unique=True)
    diachi = models.CharField(max_length=150, null=False)
    ngaysinh = models.DateField(null=True)
    gioitinh = models.CharField(max_length=20, null=False)


class SinhVien(User):
    mssv = models.CharField(max_length=30, null=False, unique=True)
    gpa = models.FloatField()
    nganh = models.ForeignKey('Nganh', on_delete=models.CASCADE, related_name='SinhVien_Nganh')
    nienkhoa = models.ForeignKey('NienKhoa', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Sinh Vien'
        verbose_name = 'Sinh Vien'


class GiaoVu(User):
    chucvu = models.CharField(max_length=30, null=False)

    class Meta:
        verbose_name_plural = 'Giao Vu'
        verbose_name = 'Giao Vu'


class Khoa(models.Model):
    ten_khoa = models.CharField(max_length=100, unique=True, null=False)
    mota = models.CharField(max_length=255, null=True)
    namthanhlap = models.DateField()

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
    ten_nienkhoa = models.CharField(max_length=25, null=False)
    nam_batdau = models.DateField()
    nam_ketthuc = models.DateField()

    def __str__(self):
        return self.nam_batdau, self.nam_ketthuc

    class Meta:
        verbose_name_plural = 'Nien Khoa'
        verbose_name = 'Nien Khoa'


class GiangVien(User):
    hocham = models.CharField(max_length=25, null=False)
    khoa = models.ForeignKey(Khoa, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Giang Vien'
        verbose_name = 'Giang Vien'


class HoiDong(models.Model):
    chutich = models.ForeignKey(GiangVien, on_delete=models.CASCADE, related_name='hoidong_chutichvien')
    thuky = models.ForeignKey(GiangVien, on_delete=models.CASCADE, related_name='hoidong_thuky')
    phanbien = models.ForeignKey(GiangVien, on_delete=models.CASCADE, related_name='hoidong_phanbien')
    giangvien = models.ManyToManyField('GiangVien', related_name='hoidong_giangvien')
    khoaluan = models.ManyToManyField('KhoaLuan', related_name='hoidong_khoaluan')
    # trangthai = models.CharField(max_length=50, null=False)

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
    ten_khoaluan = models.CharField(max_length=155)
    mo_ta = models.CharField(max_length=255)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_capnhat = models.DateTimeField(auto_now=True)
    nganh = models.ForeignKey(Nganh, on_delete=models.CASCADE)
    hoidong = models.ForeignKey(HoiDong, on_delete=models.PROTECT, related_name='khoaluan_hoidong')
    giangvien = models.ManyToManyField(GiangVien, related_name='khoaluan_giangvien')
    sinhvien = models.ManyToManyField(SinhVien, related_name='khoaluan_sinhvien')
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
    sodiem = models.FloatField()
    nhanxet = RichTextField(null=True)

    class Meta:
        verbose_name_plural = 'Diem'
        verbose_name = 'Diem'
