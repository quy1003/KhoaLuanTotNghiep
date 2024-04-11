from django.contrib import admin
from django.urls import path,re_path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('khoas', views.KhoaViewset, basename='khoas')
router.register('hoidongs', views.HoiDongViewset, basename='hoidongs')
router.register('tvhds', views.ThanhVienHoiDongViewset, basename='tvhds')


urlpatterns = [
    path('', include(router.urls)),

]
