# Generated by Django 3.1.5 on 2021-01-11 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210111_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='refferal_code',
            field=models.CharField(blank=True, default='3c2c5', max_length=150),
        ),
    ]