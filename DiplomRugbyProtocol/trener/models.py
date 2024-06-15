from django.db import models
from django.contrib.auth import models as mod

# Create your models here.
class Team(models.Model):
    Name=models.TextField()
    TShirts=models.TextField()
    Pants=models.TextField()
    City=models.TextField()
    Trener=models.ForeignKey(mod.User,related_name='team', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.Name

class Player(models.Model):
    FName=models.TextField(max_length=100) 
    SName=models.TextField(max_length=100, blank=True) 
    LName=models.TextField(max_length=100) 
    Team=models.ForeignKey(Team, related_name='teamdetail', on_delete=models.CASCADE)
    Number=models.TextField() 
    Capitan=models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return f'игрок № {self.Number} {self.LName} {self.FName} {self.SName} из команды {self.Team}'

class PlayerDetails(models.Model):
    playerId=models.ForeignKey(Player,related_name='details', on_delete=models.CASCADE)
    change=models.TimeField()
    attempts=models.IntegerField()
    realization=models.IntegerField()
    penalty=models.IntegerField()
    dropgols=models.IntegerField()
    
    class Meta:
        verbose_name = 'Детали Игрока'
        verbose_name_plural = 'Детали Игроков'
    
    def __str__(self):
        return f'Детали Игрока {self.playerId}'


class Injuries(models.Model):
    PlayerID=models.ForeignKey(Player,related_name='injuries', on_delete=models.CASCADE)
    Details=models.TextField()

    class Meta:
        verbose_name = 'Травма'
        verbose_name_plural = 'Травмы'

    def __str__(self):
        return f'Травмы Игрока {self.PlayerID}'