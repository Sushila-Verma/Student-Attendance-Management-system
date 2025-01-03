# Generated by Django 3.2.12 on 2024-08-03 07:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('attendapp', '0004_alter_students_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], max_length=15)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendapp.students')),
            ],
        ),
    ]
