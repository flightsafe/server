# Generated by Django 4.0.4 on 2022-05-16 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import plane.constants


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='maintenance', max_length=128)),
                ('description', models.TextField(help_text='Maintenance record description')),
                ('progress', models.CharField(choices=[('PENDING', 'pending'), ('IN_PROGRESS', 'in progress'), ('FINISHED', 'finished')], default=plane.constants.MaintenanceProgress['pending'], max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Plane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceRecordItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('expire_at', models.DateTimeField(null=True)),
                ('maintenance_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plane.maintenancerecord')),
                ('operator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='plane',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plane.plane'),
        ),
    ]
