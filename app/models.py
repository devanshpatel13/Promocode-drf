from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
# Create your models here.
from rest_framework.validators import UniqueValidator

CHOICES = (
    ('male', 'male'),
    ('female', 'female')
)

Discount = (
    ('flat', 'flat'),
    ('percentage', 'percentage')
)


# class Creation(AbstractUser):
#     gender = models.CharField(max_length=40, choices=CHOICES)
#     birthdate = models.DateField(null=True, blank=True)


class User(AbstractUser):
    # phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=40, choices=CHOICES)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.username)


class Coupon(models.Model):
    Coupon_REGEX = RegexValidator("[A-Z]+", 'USE CAPITAL LETTER')
    coupon = models.CharField(max_length=6, validators=[Coupon_REGEX])
    create_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=CHOICES)
    discount = models.IntegerField()
    discount_type = models.CharField(max_length=20, choices=Discount)
    # active = models.BooleanField(default=True)
    user_limit = models.IntegerField()
    coupon_limit = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    def validate(self):
        if self.create_date < self.expiry_date:
            raise ValidationError("please change date, b'cos your expiry date is less then create date ")
    def __str__(self):
        return self.coupon


class Product(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    total = models.IntegerField()


