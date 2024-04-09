from django.contrib import admin
from django.urls import path,re_path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('sinhvien',views.SinhVienViewset)
router.register('giangvien',views.GiangVienViewset)

#/courses/-GET
#/courses/-POST
#/courses/{course_id}/ GET
#/courses/{course_id}/ PUT

urlpatterns = [
    path('', include(router.urls)),

]
