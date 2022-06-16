# Generated by Django 4.0.5 on 2022-06-15 10:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='coupon',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.coupon'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='total',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coupon',
            name='coupon',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('[A-Z]+', 'only valid email is required')]),
        ),
    ]