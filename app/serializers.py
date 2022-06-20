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

        code = Coupon.objects.get(coupon=coupon)
        user = self.context.get('request').user
        birthdate = User.objects.filter(birthdate=user.birthdate).first()

        expiry_date = coupon.expiry_date
        print(expiry_date, "fffffffffffffffffff")
        validdate = datetime.datetime.now().strftime("%m-%d-%y")
        if code.discount_type == "flat":
            total = price - code.discount
        else:
            birthdate = birthdate.birthdate
            validdate = datetime.datetime.now().strftime("%m-%d")

            if birthdate and birthdate.strftime("%m-%d") == validdate:
                discount = price * (code.discount / 100)
                discount_price = price - discount
                total = discount_price - (discount_price * 0.1)
            else:
                discount = price * (code.discount / 100)
                total = price - discount
        coupon_max_limit = code.coupon_limit
        user_limit = code.user_limit

        if user.is_authenticated:
            # raise serializers.ValidationError("choose different coupon or coupon limit is over")

            user_count = len(Product.objects.filter(user=user, coupon=code))
            coupon_count = len(Product.objects.filter(coupon=code))
            # import pdb;
            # pdb.set_trace()
            if user_count >= user_limit:
                raise serializers.ValidationError("Per user  limit is over")

            if coupon_max_limit <= coupon_count:
                raise serializers.ValidationError("Coupon limit is over")

            code.max_limit = code.coupon_limit - 1
            code.save()
        else:
            raise serializers.ValidationError("coupon limit is oveeeeeeeeeeeeeeeeee")

        attrs['coupon'] = code
        attrs['user_id'] = user.id
        attrs['total'] = total
        if expiry_date.strftime("%m-%d-%y") < validdate:
            raise serializers.ValidationError("Coupon has been expired")
        return attrs


class Couponserializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['coupon', 'create_date', 'expiry_date', 'user', 'gender', 'discount', 'discount_type', 'user_limit',
                  'coupon_limit']
        raed_only_field = ['is_active']
