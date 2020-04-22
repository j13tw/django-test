from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
# from vnfPackage.views import hello_world, hello_world_template

router = DefaultRouter()
router.register(r'vnf_packages', views.VnfPkgInfoView)

urlpatterns = [
    path('', include(router.urls))
]

