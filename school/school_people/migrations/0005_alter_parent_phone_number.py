# Generated by Django 4.2.10 on 2024-04-17 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_people', '0004_parent_email_parent_school_student_school_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='phone_number',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
    ]