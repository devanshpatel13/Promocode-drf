from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser,User

# Create your models here.
from rest_framework.validators import UniqueValidator

CHOICES = (
    ('male', 'male'),
    ('female', 'female')
)

Discount = (
    ('flat','flat'),
    ('percentage','percentage')
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
    Coupon_REGEX = RegexValidator("[A-Z]+", 'only valid email is required')
    coupon = models.CharField(max_length=6, validators=[Coupon_REGEX])
    create_date = models.DateField()
    expiry_date = models.DateField()
    user = models.ForeignKey(User, related_name= "user" , on_delete =models.CASCADE)
    gender = models.CharField(max_length=20, choices=CHOICES)
    discount = models.IntegerField()
    discount_type = models.CharField(max_length=20 ,choices=Discount)
    active = models.BooleanField()
    user_limit = models.IntegerField()
    max_user =  models.IntegerField()

    def __str__(self):
        return self.coupon

class Product(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    total = models.IntegerField()



