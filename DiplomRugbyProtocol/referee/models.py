from django.db import models

from trener.models import Player,Team

# Create your models here.
class Match(models.Model):
    TeamA=models.ForeignKey(Team, related_name='teamA', on_delete=models.CASCADE)
    TeamB=models.ForeignKey(Team, related_name='teamB', on_delete=models.CASCADE)
    StartTime=models.TimeField()
    EndTime=models.TimeField(blank=True,null=True)
    ScoreA=models.IntegerField(blank=True,null=True)
    ScoreB=models.IntegerField(blank=True,null=True)
    Type=models.ForeignKey('MatchType',related_name='type', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'
    
    def __str__(self):
        return f'Матч {self.TeamA} против {self.TeamB}'

class MatchType(models.Model):
    Type=models.TextField()

    class Meta:
        verbose_name='Тип матча'
        verbose_name_plural = 'Типы матчей'

    def __str__(self):
        return self.Type

class Aletrs(models.Model):
    MatchID=models.ForeignKey(Match, related_name='alerts', on_delete=models.CASCADE)
    PlayerID=models.ForeignKey(Player,related_name='alerts', on_delete=models.CASCADE)
    Reazon=models.TextField()

    class Meta:
        verbose_name="Предупреждение"
        verbose_name_plural="Предупреждения"

    def __str__(self):
        return f'Пердупреждение игрока № {self.PlayerID.Number} {self.PlayerID} из команды {self.PlayerID.Team}'

class Deletes(models.Model):
    MatchID=models.ForeignKey(Match, related_name='deletes', on_delete=models.CASCADE)
    PlayerID=models.ForeignKey(Player,related_name='deletes', on_delete=models.CASCADE)
    Reazon=models.TextField()

    class Meta:
        verbose_name="Удаление"
        verbose_name_plural="Удаления"
    
    def __str__(self):
        return f'Удаление игрока № {self.PlayerID.Number} {self.PlayerID} из команды {self.PlayerID.Team}'

class Changes(models.Model):
    MatchID=models.ForeignKey(Match, related_name='changes_on_match', on_delete=models.CASCADE)
    ChangedPlayerID=models.ForeignKey(Player,related_name='changed_player', on_delete=models.CASCADE)
    NewPlayerID=models.ForeignKey(Player,related_name='new_player', on_delete=models.CASCADE)

    class Meta:
        verbose_name="Замены"
        verbose_name_plural="Замены"
    
    def __str__(self):
        return f'Замена игрока {self.ChangedPlayerID} на {self.NewPlayerID}'
    
class GolsTypes(models.Model):
    GolTypeName=models.CharField(max_length=12)
    Points=models.IntegerField()

    class Meta:
        verbose_name="Тип Гола"
        verbose_name_plural="Типы голов"
    
    def __str__(self):
        return f'{self.GolTypeName}'
    
class Gols(models.Model):
    MatchID=models.ForeignKey(Match, related_name='gols_on_match', on_delete=models.CASCADE)
    Time=models.TimeField()
    GolTypeA=models.ForeignKey(GolsTypes, related_name='gols_type', on_delete=models.CASCADE)
    GolType=models.CharField(max_length=12,choices=(('attempt','Попытка'),('realization','Реализация'),('penalty','Штрафной'),('dropgol','Дроп-гол')))
    PlayerID=models.ForeignKey(Player,related_name='scored_player', on_delete=models.CASCADE)

    class Meta:
        verbose_name="Гол"
        verbose_name_plural="Голы"
    
    def __str__(self):
        return f'Гол игрока {self.PlayerID} на {self.Time} минуте'
    
