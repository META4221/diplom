from .models import Player, PlayerDetails, Team
from django import forms

class PlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.fields['FName'].label = 'Имя игрока'
        self.fields['SName'].label = 'Отчество игрока'
        self.fields['LName'].label = 'Фамилия игрока'
        self.fields['Team'].label = 'Команда'
        self.fields['Number'].label = 'Номер'
        self.fields['Capitan'].label = 'Капитан'

    class Meta:
        model=Player
        fields=['FName','SName','LName', 'Team', 'Number', 'Capitan']

class PlayerDetailForm(forms.ModelForm):
    class Meta:
        model: PlayerDetails
        fields=['playerId','change','attempts','realization','penalty','dropgols']

class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['Name'].label = 'Название команды'
        self.fields['TShirts'].label = 'Цвет рубашек'
        self.fields['Pants'].label = 'Цвет шорт'
        self.fields['City'].label = 'Город'
        self.fields['Trener'].label='Тренер'

        for fields in self.fields:
            self.fields[fields].widget.attrs['class']='team h2'


    class Meta:
        model=Team
        fields=['Name','TShirts','Pants', 'City','Trener']