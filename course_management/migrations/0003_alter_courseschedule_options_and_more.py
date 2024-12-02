# Generated by Django 4.2.3 on 2024-12-02 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course_management', '0002_courseapplication'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseschedule',
            options={'ordering': ['date', 'time_slot']},
        ),
        migrations.AlterUniqueTogether(
            name='courseschedule',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='course',
            name='lecturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_taught', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='status',
            field=models.CharField(choices=[('SCHEDULED', 'Scheduled'), ('CANCELLED', 'Cancelled'), ('COMPLETED', 'Completed')], default='SCHEDULED', max_length=20),
        ),
    ]
