# Generated by Django 5.0.4 on 2024-04-20 06:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FName', models.TextField(max_length=100)),
                ('SName', models.TextField(blank=True, max_length=100)),
                ('LName', models.TextField(max_length=100)),
                ('Number', models.TextField()),
                ('Capitan', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.TextField()),
                ('TShirts', models.TextField()),
                ('Pants', models.TextField()),
                ('City', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Injuries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Details', models.TextField()),
                ('PlayerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='injuries', to='trener.player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change', models.TimeField()),
                ('attempts', models.IntegerField()),
                ('realization', models.IntegerField()),
                ('dropgols', models.IntegerField()),
                ('playerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='trener.player')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='Team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='trener.team'),
        ),
    ]
