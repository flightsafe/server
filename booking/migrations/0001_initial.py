# Generated by Django 4.0.4 on 2022-05-24 05:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plane', '0001_initial'),
        ('course', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('lesson', models.ForeignKey(blank=True, help_text='Used in the lesson', null=True, on_delete=django.db.models.deletion.CASCADE, to='course.lessonhistory')),
                ('plane', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='plane.plane')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
