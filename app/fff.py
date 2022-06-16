from rest_framework import serializers
from .models import Coupon, Order, Userprofile
import datetime
from django.utils import timezone


class CouponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'url', 'promo_code', 'discount_type', 'discount', 'per_user_limit', 'max_limit', 'start_date',
                  'expiry_date', 'owner']

    def validate(self, data):
        if data['discount'] > 100:
            if data['discount_type'] == 'percentage':
                raise serializers.ValidationError("Enter a valid discount")
        return data


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    code = serializers.CharField(required=True)

    class Meta:
        model = Order
        fields = ['code', 'order_amount', 'total_amount']
        read_only_fields = ['total_amount']

    def validate(self, attrs):
        code = attrs.pop('code', None)
        order_amount = attrs.get('order_amount', None)
        if not Coupon.objects.filter(promo_code=code).exists():
            raise serializers.ValidationError("Coupon code not found!")

        coupon = Coupon.objects.get(promo_code=code)
        user = self.context.get('request').user
        user_birth = Userprofile.objects.filter(birth_date=user.birth_date).first()

        if coupon.discount_type == "flat":
            total_amount = order_amount - coupon.discount
        else:
            birthdate = user_birth.birth_date
            valid_date = timezone.now().date().strftime("%m-%d")

            if birthdate and birthdate.strftime("%m-%d") == valid_date:
                discount = order_amount * (coupon.discount / 100)
                total = order_amount - discount
                total_amount = total - (total * 0.1)

            else:
                discount = order_amount * (coupon.discount / 100)
                total_amount = order_amount - discount

        coupon_max_limit = coupon.max_limit
        user_limit = coupon.per_user_limit

        if user.is_authenticated:
            user_count = len(Order.objects.filter(user=user, code=coupon))
            coupon_count = len(Order.objects.filter(code=coupon))

            if coupon_count > user_limit:
                raise serializers.ValidationError("Coupon limit is over")

            if user_count > coupon_max_limit:
                raise serializers.ValidationError("Per user limit is over")

            coupon.max_limit = coupon.max_limit - 1
            coupon.save()


        else:
            raise serializers.ValidationError("Coupon limit is over")

        attrs['code'] = coupon
        attrs['user_id'] = user.id
        attrs['total_amount'] = total_amount
        return attrs

    # def save(self, **kwargs):
    #     self.validated_data['user_id'] = self.validated_data['user_id'].id
    #
    #     # self.validated_data['user_id'] = self.validated_data['user_id'].birth_date
    #
    #     return super(OrderSerializer, self).save(**kwargs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = ['username', 'birth_date', 'gender']