# Generated by Django 5.0.4 on 2024-05-17 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referee', '0005_gols'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='EndTime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='match',
            name='StartTime',
            field=models.TimeField(),
        ),
    ]