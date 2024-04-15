from django.contrib import admin
from django.urls import path,re_path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('khoas', views.KhoaViewset, basename='khoas')
router.register('hoidongs', views.HoiDongViewset, basename='hoidongs')
router.register('users', views.UserViewset, basename='users')
router.register('hoidongdetail', views.HoiDongDetailViewset,basename='hoidongdetail')
router.register('khoa_khoaluans', views.Khoa_KhoaLuanViewset, basename='khoa_khoaluans')
router.register('diems', views.DiemViewset, basename='diems')
router.register('diem_detail', views.DiemDetailViewset, basename='diem_detail')
urlpatterns = [
    path('', include(router.urls)),

]
