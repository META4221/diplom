# Generated by Django 5.0.4 on 2024-05-16 11:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referee', '0004_remove_match_score_match_scorea_match_scoreb'),
        ('trener', '0003_playerdetails_penalty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gols',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Time', models.TimeField()),
                ('GolType', models.CharField(choices=[('attempt', 'Попытка'), ('realization', 'Реализация'), ('penalty', 'Штрафной'), ('dropgol', 'Дроп-гол')], max_length=12)),
                ('MatchID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gols_on_match', to='referee.match')),
                ('PlayerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scored_player', to='trener.player')),
            ],
            options={
                'verbose_name': 'Гол',
                'verbose_name_plural': 'Голы',
            },
        ),
    ]