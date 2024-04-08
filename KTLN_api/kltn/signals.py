#Chuc Năng Send-email
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import HoiDong, GiangVien
from django.conf import settings


@receiver(m2m_changed, sender=HoiDong.giangvien.through)
def send_email_to_giangvien(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        giangviens = kwargs['pk_set']
        for giangvien_id in giangviens:
            giangvien = GiangVien.objects.get(pk=giangvien_id)
            subject = 'Thông báo: Bạn đã được thêm vào hội đồng'
            message = 'Chào {},\n\nBạn đã được thêm vào hội đồng thành công.'.format(giangvien.username)
            send_mail(subject, message, settings.EMAIL_HOST_USER, [giangvien.email])