# Generated by Django 5.0.4 on 2024-05-17 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referee', '0006_alter_match_endtime_alter_match_starttime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='EndTime',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='ScoreA',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='ScoreB',
            field=models.IntegerField(blank=True),
        ),
    ]