# Generated by Django 4.0.4 on 2022-05-24 05:06

import common.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('CREATE_BOOKING', 'Create Booking'), ('DELETE_BOOKING', 'Delete Booking'), ('CREATE_LESSON_RECORD', 'Create Lesson Record'), ('CREATE_COMMENT', 'Create Comment'), ('ADD_MAINTENANCE_ITEM', 'Add Maintenance Item'), ('CHANGE_MAINTENANCE_STATUS', 'Change Maintenance Status'), ('START_MAINTENANCE', 'Start Maintenance'), ('END_MAINTENANCE', 'End Maintenance')], max_length=128)),
                ('details', common.fields.DataclassJSONField(help_text='Transaction details')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
