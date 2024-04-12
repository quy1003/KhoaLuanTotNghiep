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
                                       ,related_name='thanhviens',
                                       through='ThanhVien_HoiDong')
    class Meta:
        verbose_name_plural = 'Hoi Dong'
        verbose_name = 'Hoi Dong'

    def __str__(self):
        return self.ten

    def update_trangthai(self):
        if self.thanhviens.count() >=3:
            self.trangthai = True;
        else:
            self.trangthai = False;
        self.save()

class ThanhVien_HoiDong(models.Model):
    roles = (
        ('CHU TICH', 'chu tich'),
        ('THU KY', 'thu ky'),
        ('PHAN BIEN', 'phan bien'),
        ('THANH VIEN KHAC', 'thanh vien khac')
    )
    thanhvien = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'chucvu': 'giangvien'})
    hoidong = models.ForeignKey(HoiDong, on_delete=models.CASCADE)
    vaitro = models.CharField(choices=roles, null=False, max_length=100,default='THANH VIEN KHAC')

    class Meta:
        unique_together = ['thanhvien', 'hoidong']
        verbose_name_plural = 'Thanh Vien - Hoi Dong'
        verbose_name = 'Thanh Vien - Hoi Dong'

    def clean(self):
        super().clean()
        count_thanhvien_hoidong = self.hoidong.thanhviens.count()
        if count_thanhvien_hoidong == 5:
            raise ValidationError('Lỗi: Hội đồng đã đủ số lượng thành viên.')
        existing_chu_tich = ThanhVien_HoiDong.objects.filter(hoidong=self.hoidong, vaitro='CHU TICH').exists()
        existing_thu_ky = ThanhVien_HoiDong.objects.filter(hoidong=self.hoidong, vaitro='THU KY').exists()
        existing_phan_bien = ThanhVien_HoiDong.objects.filter(hoidong=self.hoidong, vaitro='PHAN BIEN').exists()

        if self.vaitro == 'CHU TICH' and existing_chu_tich:
            raise ValidationError('Lỗi: Hội đồng này đã có chức vụ Chủ tịch.')
        elif self.vaitro == 'THU KY' and existing_thu_ky:
            raise ValidationError('Lỗi: Hội đồng này đã có chức vụ Thư ký.')
        elif self.vaitro == 'PHAN BIEN' and existing_phan_bien:
            raise ValidationError('Lỗi: Hội đồng này đã có chức vụ Phản biện.')


class Khoa(models.Model):
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
    gv_huongdan = models.ManyToManyField(User, related_name='gv_huongdans', limit_choices_to={'chucvu':'giangvien'})
    sinhvien = models.ManyToManyField(User, related_name='sinhviens',limit_choices_to={'chucvu': 'hocsinh'})
    trangthai = models.BooleanField(default=1)

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
