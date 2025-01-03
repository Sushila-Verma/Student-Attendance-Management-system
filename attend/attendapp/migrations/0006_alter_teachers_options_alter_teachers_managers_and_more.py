# Generated by Django 4.1.13 on 2024-08-04 07:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendapp', '0005_attendance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teachers',
            options={},
        ),
        migrations.AlterModelManagers(
            name='teachers',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='Subject',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='password',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='username',
        ),
        migrations.AddField(
            model_name='teachers',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='attendapp.students'),
        ),
    ]