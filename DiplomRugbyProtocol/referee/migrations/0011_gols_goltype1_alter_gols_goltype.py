# Generated by Django 5.0.4 on 2024-06-14 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referee', '0010_alter_gols_goltype'),
    ]

    operations = [
        migrations.AddField(
            model_name='gols',
            name='GolType1',
            field=models.CharField(choices=[('attempt', 'Попытка'), ('realization', 'Реализация'), ('penalty', 'Штрафной'), ('dropgol', 'Дроп-гол')], default=1, max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gols',
            name='GolType',
            field=models.CharField(choices=[('attempt', 'Попытка'), ('realization', 'Реализация'), ('penalty', 'Штрафной'), ('dropgol', 'Дроп-гол')], max_length=12),
        ),
    ]
