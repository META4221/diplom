import os
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
import datetime
from trener.models import Player
from .models import Changes,Aletrs,Match,Gols,Deletes
from .forms import AlertsForm, ChangeForm, DeletesForm, MatchForm, GolForm
from docxtpl import DocxTemplate

def scoreCount(id):
    gols=Gols.objects.filter(MatchID=id)
    total_gols_a,total_gols_b=0,0
    for i in gols:
        if i.PlayerID.Team == i.MatchID.TeamA:
            total_gols_a+=i.GolTypeA.Points
        else:
            total_gols_b+=i.GolTypeA.Points
    return {'GolsB':total_gols_b,'GolsA':total_gols_a}

def match_list(request):
    match_l=Match.objects.all()
    p={}
    for i in match_l:
        print(i.id)
        p[i.id] = scoreCount(i.id)
    # print(p['Матч Тигры против team 2'])    
    return render(request,'match.html',{'matches':match_l,"score":p})

def matchDetail(request, id):
    match=get_object_or_404(Match, id=id)
    with connection.cursor() as cursor:
        
        alerts=Aletrs.objects.filter(MatchID=id)
        gols=Gols.objects.filter(MatchID=id)
        deletes=Deletes.objects.filter(MatchID=id)
        changes=Changes.objects.filter(MatchID=id)
        
        total_gols_a,total_gols_b=0,0
        for i in gols:
            if i.PlayerID.Team == i.MatchID.TeamA:
                total_gols_a+=i.GolTypeA.Points
            else:
                total_gols_b+=i.GolTypeA.Points

    match_l=Match.objects.filter(id=id)

    return render(request, 'matchdetail.html',{'Gols':gols,'GolsB':total_gols_b,'GolsA':total_gols_a,'alerts':alerts,'Match':match_l, 'Deletes':deletes, 'Changes':changes, 'matchid':id})

def save(request,id):
    print('save')

    with connection.cursor() as cursor:
        cursor.execute("SELECT Reazon, LName, Name FROM referee_aletrs a join trener_player p on a.playerId_id =p.id join trener_team t on p.Team_id=t.id where MatchID_id=%s",[id])
        rowsA=cursor.fetchall()
        cursor.execute("select Reazon,LName,trener_team.Name from referee_aletrs,trener_player,trener_team, referee_match where referee_aletrs.PlayerID_id=trener_player.id and trener_player.Team_id=trener_team.id and trener_team.id=referee_match.TeamB_id and referee_aletrs.MatchID_id=%s",[id])
        rowsB=cursor.fetchall()
        cursor.execute("select Reazon,LName,trener_team.Name, MatchID_id from referee_deletes, trener_player,trener_team WHERE referee_deletes.PlayerID_id=trener_player.id and trener_player.Team_id=trener_team.id and MatchID_id=%s",[id])
        deletes=cursor.fetchall()
        cursor.execute("select LName,referee_gols.Time, GolType from referee_gols,trener_player,trener_team, referee_match where referee_gols.PlayerID_id=trener_player.id and trener_player.Team_id=trener_team.id and trener_team.id=referee_match.TeamA_id and referee_match.id=%s",[id])
        goalsA=cursor.fetchall()
        cursor.execute("select LName,referee_gols.Time, GolType from referee_gols,trener_player,trener_team, referee_match where referee_gols.PlayerID_id=trener_player.id and trener_player.Team_id=trener_team.id and trener_team.id=referee_match.TeamB_id and referee_match.id=%s",[id])
        goalsB=cursor.fetchall()
        
        cursor.execute("SELECT g.time, g.GolType, g.MatchID_id, p.LName, t.name FROM referee_gols g JOIN trener_player p ON g.playerId_id = p.id JOIN trener_team t ON p.Team_id = t.id where MatchID_id=%s",[id])
        gols=cursor.fetchall()

        cursor.execute("select StartTime from referee_match where referee_match.id=%s",[id])
        matchData=cursor.fetchall()
        
        cursor.execute("SELECT p1.LName, p2.LName , pr.MatchID_id, t.name FROM referee_changes pr JOIN trener_player p1 ON pr.ChangedPlayerID_id = p1.id JOIN trener_player p2 ON pr.NewPlayerID_id = p2.id JOIN trener_team t on p1.Team_id=t.id WHERE MatchID_id=%s",[id])
        changes=cursor.fetchall()

        # print(gols)
        
    teamA={'points1':{'attempts':0, 'penalty':0, 'dropgol':0, 'realization':0, 'total':0},
           'points2':{'attempts':0, 'penalty':0, 'dropgol':0, 'realization':0, 'total':0},
           'overtime':{'attempts':0, 'penalty':0, 'dropgol':0, 'realization':0, 'total':0}
    }
    for i in goalsA:
        delta = datetime.datetime.combine(datetime.date.today(), i[1]) - datetime.datetime.combine(datetime.date.today(), matchData[0][0])
        if delta.total_seconds() / 60 <= 40:
            if i[2] == 'attempt':
                teamA['points1']['attempts'] += 5
                teamA['points1']['total'] += 5
            elif i[2] == 'penalty':
                teamA['points1']['penalty'] += 3
                teamA['points1']['total'] += 3
            elif i[2] == 'dropgol':
                teamA['points1']['dropgol'] += 3
                teamA['points1']['total'] += 3
            elif i[2] == 'realization':
                teamA['points1']['realization'] += 7
                teamA['points1']['total'] += 7
        elif delta.total_seconds() / 60 >= 40:
            if i[2] == 'attempt':
                teamA['points2']['attempts'] += 5
                teamA['points2']['total'] += 5
            elif i[2] == 'penalty':
                teamA['points2']['penalty'] += 3
                teamA['points2']['total'] += 3
            elif i[2] == 'dropgol':
                teamA['points2']['dropgol'] += 3
                teamA['points2']['total'] += 3
            elif i[2] == 'realization':
                teamA['points2']['realization'] += 7
                teamA['points2']['total'] += 7
        else:
            if i[2] == 'attempt':
                teamA['overtime']['attempts'] += 5
                teamA['overtime']['total'] += 5
            elif i[2] == 'penalty':
                teamA['overtime']['penalty'] += 3
                teamA['overtime']['total'] += 3
            elif i[2] == 'dropgol':
                teamA['overtime']['dropgol']+= 3
                teamA['overtime']['total'] += 3
            elif i[2] == 'realization':
               teamA['overtime']['realization'] += 7
               teamA['overtime']['total'] += 7

    teamB={'points1':{'attempts':0, 'penalty':0, 'dropgol':0, 'realization':0, 'total':0},
           'points2':{'attempts':0, 'penalty':0, 'dropgol':0, 'realization':0, 'total':0},
           'overtime':{'attempts':0, 'penalty':0, 'dropgol':0, 'realization':0, 'total':0}
    }
    for i in goalsB:
        delta = datetime.datetime.combine(datetime.date.today(), i[1]) - datetime.datetime.combine(datetime.date.today(), matchData[0][0])
        if delta.total_seconds() / 60 <= 40:
            if i[2] == 'attempt':
                teamB['points1']['attempts'] += 5
                teamB['points1']['total'] += 5
            elif i[2] == 'penalty':
                teamB['points1']['penalty'] += 3
                teamB['points1']['total'] += 3
            elif i[2] == 'dropgol':
                teamB['points1']['dropgol'] += 3
                teamB['points1']['total'] += 3
            elif i[2] == 'realization':
                teamB['points1']['realization'] += 7
                teamB['points1']['total'] += 7
        elif delta.total_seconds() / 60 >= 40:
            if i[2] == 'attempt':
                teamB['points2']['attempts'] += 5
                teamB['points2']['total'] += 5
            elif i[2] == 'penalty':
                teamB['points2']['penalty'] += 3
                teamB['points2']['total'] += 3
            elif i[2] == 'dropgol':
                teamB['points2']['dropgol'] += 3
                teamB['points2']['total'] += 3
            elif i[2] == 'realization':
                teamB['points2']['realization'] += 7
                teamB['points2']['total'] += 7
        else:
            if i[2] == 'attempt':
                teamB['overtime']['attempts'] += 5
                teamB['overtime']['total'] += 5
            elif i[2] == 'penalty':
                teamB['overtime']['penalty'] += 3
                teamB['overtime']['total'] += 3
            elif i[2] == 'dropgol':
                teamB['overtime']['dropgol']+= 3
                teamB['overtime']['total'] += 3
            elif i[2] == 'realization':
               teamB['overtime']['realization'] += 7
               teamB['overtime']['total'] += 7

    match_l=Match.objects.filter(id=id)

    doc = DocxTemplate('templates/test.docx')
    context={'test':'testasdas',
             't':request,
             'Changes':changes,
             'Deletes':deletes,
             'Alerts':rowsA,
             'Match':match_l,
              'GoalA':teamA,'GoalB':teamB,}
    doc.render(context)
    user_download_dir = os.path.expanduser('~\Downloads')
    print(user_download_dir)
    doc.save(''+user_download_dir+f'\{match_l.get().TeamA.Name} vs {match_l.get().TeamB.Name}.docx')
    
    return(render(request,'save.html'))

def add_change(request,id):
    if request.method == 'POST':
        form =ChangeForm(request.POST)
        if form.is_valid():
            form.MatchID = id
            form.save()
            return redirect(request.session.get('prev_page', '/')) 
    else:
        form = ChangeForm(initial={'MatchID':id})
    request.session['prev_page'] = request.META.get('HTTP_REFERER', '/')
    return render(request,'playerAdd.html',{'form': form})

def add_alert(request,id):
    
    if request.method == 'POST':
        form =AlertsForm(request.POST)
        if form.is_valid():
            form.save()
            # request.META.get('HTTP_REFERER', '/') эта часть подойдет для обновления страници при добвалении еще одного  
            return redirect(request.session.get('prev_page', '/'))  # Redirect to player list after successful form submission
    else:
        form = AlertsForm(initial={'MatchID':id})
    request.session['prev_page'] = request.META.get('HTTP_REFERER', '/')
    return render(request,'playerAdd.html',{'form': form})

def add_delete(request,id):
    if request.method == 'POST':
        form =DeletesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.session.get('prev_page', '/'))  # Redirect to player list after successful form submission
    else:
        form = DeletesForm(initial={'MatchID':id})
    request.session['prev_page'] = request.META.get('HTTP_REFERER', '/')
    return render(request,'playerAdd.html',{'form': form})

def add_match(request):
    if request.method == 'POST':
        form =MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.session.get('prev_page', '/'))  # Redirect to player list after successful form submission
    else:
        form = MatchForm()
    request.session['prev_page'] = request.META.get('HTTP_REFERER', '/')
    return render(request,'playerAdd.html',{'form': form})

def add_gol(request,id):
    if request.method == 'POST':
        form =GolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.session.get('prev_page', '/'))  # Redirect to player list after successful form submission
    else:
        form = GolForm(initial={'MatchID':id})
    request.session['prev_page'] = request.META.get('HTTP_REFERER', '/')
    return render(request,'playerAdd.html',{'form': form})