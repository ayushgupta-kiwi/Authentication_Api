# Generated by Django 4.1.6 on 2023-02-13 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student_Details', '0005_alter_student_info_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_info',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]
