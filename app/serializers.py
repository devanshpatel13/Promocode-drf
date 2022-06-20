import datetime

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from django.utils import timezone


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'gender', 'birthdate']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gender=validated_data['gender'],
            birthdate=validated_data['birthdate']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class Productserializers(serializers.ModelSerializer):
    # total = serializers.SerializerMethodField('get_discount')
    # coupon = serializers.CharField(required=True)

    class Meta:
        model = Product
        fields = ['coupon', 'user', 'price', 'name', 'total']
        read_only_fields = ["total"]

    def validate(self, attrs):
        coupon = attrs.pop('coupon', None)
        price = attrs.get('price', None)
        if not Coupon.objects.filter(coupon=coupon).exists():
            raise serializers.ValidationError("Coupon code not found!")

        coupon = Coupon.objects.get(coupon=coupon)
        user = self.context.get('request').user
        birthdate = User.objects.filter(birthdate=user.birthdate).first()

        expiry_date = coupon.expiry_date
        print(expiry_date,"fffffffffffffffffff")
        validdate = datetime.datetime.now().strftime("%m-%d-%y")
        if coupon.discount_type == "flat":
            total = price - coupon.discount
        else:
            birthdate = birthdate.birthdate
            validdate = datetime.datetime.now().strftime("%m-%d")


            if birthdate and birthdate.strftime("%m-%d") == validdate:
                discount = price * (coupon.discount / 100)
                discount_price = price - discount
                total = discount_price - (discount_price * 0.1)
            else:
                discount = price * (coupon.discount / 100)
                total = price - discount
        coupon_use_limit = coupon.max_user
        coupon_usee_limit = coupon.user_limit

        if not user.is_authenticated:
            raise serializers.ValidationError("choose different coupon or coupon limit is over")

        user_count = len(Product.objects.filter(user=user, coupon=coupon))
        coupon_count = len(Product.objects.filter(coupon=coupon))

        if coupon_count > coupon_usee_limit:
            raise serializers.ValidationError("Coupon limit is over")

        if user_count > coupon_use_limit:
            raise serializers.ValidationError("Per user limit is over")

        coupon.max_limit = coupon.max_user - 1
        coupon.save()
        attrs['coupon'] = coupon
        attrs['user_id'] = user.id
        attrs['total'] = total
        if expiry_date.strftime("%m-%d-%y") < validdate:
            raise serializers.ValidationError("Coupon has been expired")
        return attrs




class Couponserializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['coupon', 'create_date', 'expiry_date', 'user', 'gender', 'discount', 'discount_type', 'user_limit',
                  'max_user']
        raed_only_field = ['is_active']
