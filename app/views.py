from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import *


# Create your views here.

class CreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    # @csrf_exempt
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer, "ffffffffffffffffffffff")
    #     serializer.is_valid(raise_exception=True)
    #     print(serializer)
    #     self.perform_create(serializer)
    #     # headers = self.get_success_headers(serializer.data)
    #     return JsonResponse(serializer.data)




@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return JsonResponse({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    return JsonResponse({'user_id': user.pk},
                    status=status.HTTP_200_OK)





class ProductView(generics.ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = Productserializers

class CouponView(generics.ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = Couponserializer



class CouponupdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = Couponserializer
    # lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        id = kwargs["pk"]
        coupon = Coupon.objects.get(id = id)
        user_count = len(Product.objects.filter(coupon=coupon))
        if user_count == 0:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return JsonResponse(serializer.data)
        else:
            print("sssssssssssssssss")
            return JsonResponse({'msg':'sssssssssssssss'})
