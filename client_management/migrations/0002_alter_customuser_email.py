# Generated by Django 4.2.3 on 2024-12-03 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
    ]