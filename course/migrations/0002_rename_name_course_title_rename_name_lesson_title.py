# Generated by Django 4.0.4 on 2022-05-30 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='name',
            new_name='title',
        ),
    ]
