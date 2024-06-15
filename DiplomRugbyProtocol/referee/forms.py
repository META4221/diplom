from .models import Aletrs,Changes,Deletes, Match, Gols, Player
from django import forms

class AlertsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlertsForm, self).__init__(*args, **kwargs)
        self.fields['MatchID'].label = 'Матч'
        self.fields['PlayerID'].label = 'Нарушивший игрок'
        self.fields['Reazon'].label = 'Нарушение'
        teams=Match.objects.values_list('TeamA_id','TeamB_id').filter(id=self.initial.get('MatchID'))

        for i in teams:
            players_in_teams = Player.objects.filter(Team_id__in=i)

        self.fields['PlayerID'].queryset = players_in_teams


    class Meta:
        model=Aletrs
        fields=['MatchID','PlayerID', 'Reazon']


class ChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChangeForm, self).__init__(*args, **kwargs)
        self.fields['MatchID'].label = 'Матч'
        self.fields['ChangedPlayerID'].label = 'Заменяемый игрок'
        self.fields['NewPlayerID'].label = 'Заменяющий игрок'

        teams=Match.objects.values_list('TeamA_id','TeamB_id').filter(id=self.initial.get('MatchID'))

        for i in teams:
            players_in_teams = Player.objects.filter(Team_id__in=i)
        self.fields['ChangedPlayerID'].queryset = players_in_teams
        self.fields['NewPlayerID'].queryset = players_in_teams

        for fields in self.fields:
            self.fields[fields].widget.attrs['class']='team h2'

    class Meta:
        model=Changes
        fields=['MatchID','ChangedPlayerID','NewPlayerID']

class DeletesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeletesForm, self).__init__(*args, **kwargs)
        self.fields['MatchID'].label = 'Матч'
        self.fields['PlayerID'].label = 'Удаленный игрок'
        self.fields['Reazon'].label = 'Причина'

        teams=Match.objects.values_list('TeamA_id','TeamB_id').filter(id=self.initial.get('MatchID'))

        for i in teams:
            players_in_teams = Player.objects.filter(Team_id__in=i)
        self.fields['PlayerID'].queryset = players_in_teams

        for fields in self.fields:
            self.fields[fields].widget.attrs['class']='team h2'

    class Meta:
        model=Deletes
        fields=['MatchID','PlayerID', 'Reazon']

class MatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['TeamA'].label = 'Команда А'
        self.fields['TeamB'].label = 'Команда Б'
        self.fields['StartTime'].label = 'Время начала матча'
        self.fields['EndTime'].label = 'Время окончания матча'
        self.fields['ScoreA'].label = 'Счет команды А'
        self.fields['ScoreB'].label = 'Счет команды Б'
        self.fields['Type'].label = 'Тип матча'

        for fields in self.fields:
            self.fields[fields].widget.attrs['class']='team h2'
    
    class Meta:
        model=Match
        fields=['TeamA','TeamB','StartTime','EndTime','ScoreA','ScoreB','Type']

class GolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GolForm, self).__init__(*args, **kwargs)
        self.fields['MatchID'].label = 'Матч'
        self.fields['Time'].label = 'Время'
        self.fields['GolType'].label = 'Тип попытки'
        self.fields['PlayerID'].label = 'Игрок'

        teams=Match.objects.values_list('TeamA_id','TeamB_id').filter(id=self.initial.get('MatchID'))

        for i in teams:
            players_in_teams = Player.objects.filter(Team_id__in=i)
        self.fields['PlayerID'].queryset = players_in_teams

        for fields in self.fields:
            self.fields[fields].widget.attrs['class']='team h2'
    
    class Meta:
        model=Gols
        fields=['MatchID','Time', 'GolType', 'PlayerID']
