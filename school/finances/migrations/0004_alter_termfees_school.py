# Generated by Django 4.2.10 on 2024-04-19 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school_people', '0005_alter_parent_phone_number'),
        ('finances', '0003_alter_termfees_end_date_alter_termfees_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termfees',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school_people.school'),
        ),
    ]
