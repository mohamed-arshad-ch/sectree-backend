# Generated by Django 3.1.5 on 2021-01-11 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='refferal_code',
            field=models.CharField(blank=True, default='130ef', max_length=150),
        ),
    ]
