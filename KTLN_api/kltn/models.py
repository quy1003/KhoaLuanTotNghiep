from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser, models.Model):
    pass


class SinhVien(User):
    pass


class GiaoVu(User):
    pass


class GiangVien(User):
    pass


class HoiDong(models.Model):
    chutich = models.ForeignKey(GiangVien, on_delete=models.CASCADE, related_name='hoidong_chutichvien')
    thuky = models.ForeignKey(GiangVien, on_delete=models.CASCADE, related_name='hoidong_thuky')
    phanbien = models.ForeignKey(GiangVien, on_delete=models.CASCADE, related_name='hoidong_phanbien')
    giangvien = models.ManyToManyField(GiangVien, related_name='hoidong_giangvien')

class Nganh(models.Model):
    ten_nganh = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name


class TieuChi(models.Model):
    ten_tieuchi = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name


class KhoaLuan(models.Model):
    giaovu = models.ForeignKey(GiaoVu, on_delete=models.PROTECT)
    ten_khoaluan = models.CharField(max_length=155)
    mo_ta = models.CharField(max_length=255)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    nganh = models.ForeignKey(Nganh, on_delete=models.CASCADE)
    hoidong = models.ForeignKey(HoiDong, on_delete=models.PROTECT)
    giangvien = models.ManyToManyField(GiangVien)
    def __str__(self):
        return self.name


class Diem(models.Model):
    giangvien = models.ForeignKey(GiangVien, on_delete=models.CASCADE)
    tieuchi = models.ForeignKey(TieuChi, on_delete=models.CASCADE)
    khoaluan = models.ForeignKey(KhoaLuan, on_delete=models.CASCADE)
    sodiem = models.IntegerField()

