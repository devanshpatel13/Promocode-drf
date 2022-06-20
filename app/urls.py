from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


from .views import *
#
# from rest_framework import routers
#
router = routers.DefaultRouter()
router.register("create", CreateView , basename = "create")

urlpatterns = [

    path('', include(router.urls)),
    # path("student", StudentViewSet.as_view(), name="student"),
    # path("create/", CreationView.as_view(),name ="mixin"),
    # path("mixinget/<id>/", StudentmixinView.as_view(),name = "mixin"),
    path('product/', ProductView.as_view(),name ="product"),
    path('coupon/',CouponView.as_view(),name = "coupon"),
    path("couponedit/<int:pk>/", CouponupdateView.as_view(), name = "couponedit"),
    path('auth', include('rest_framework.urls', namespace='rest_framework'))

]
