# Generated by Django 5.0.4 on 2024-06-16 05:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referee', '0014_gols_goltypea'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gols',
            name='GolTypeA',
        ),
        migrations.AlterField(
            model_name='gols',
            name='GolType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gols_type', to='referee.golstypes'),
        ),
    ]