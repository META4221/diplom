import os
from django.conf import settings
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
import datetime
from trener.models import Player
from .models import Changes,Aletrs,Match,Gols,Deletes
from .forms import AlertsForm, ChangeForm, DeletesForm, MatchForm, GolForm
from docxtpl import DocxTemplate

def pointsCount(i,match_l):
    Points={'points1':{'attempts':0, 'penalty':0, 'dropgol':0, 'realization':0, 'total':0},
           'points2':{'attempts':0, 'penalty':0, 'dropgol':0, 'realization':0, 'total':0},
           'overtime':{'attempts':0, 'penalty':0, 'dropgol':0, 'realization':0, 'total':0}
    }

    delta = datetime.datetime.combine(datetime.date.today(), i.Time) - datetime.datetime.combine(datetime.date.today(), match_l.get().StartTime)
    if delta.total_seconds()/60 <=40:
        match i.GolType.GolTypeName:
            case 'Попытка':
                Points['points1']['attempts'] += 5
                Points['points1']['total'] += 5
            case 'Реализация':
                Points['points1']['realization'] += 7
                Points['points1']['total'] += 3
            case 'Штрафной':
                Points['points1']['penalty'] += 3
                Points['points1']['total'] += 7
            case 'Дроп-гол':
                Points['points1']['dropgol'] += 3
                Points['points1']['total'] += 3
    elif delta.total_seconds() / 60 >= 40:
        match i.GolType:
            case 'Попытка':
                Points['points12']['attempts'] += 5
                Points['points12']['total'] += 5
            case 'Реализация':
                Points['points2']['realization'] += 7
                Points['points2']['total'] += 3
            case 'Штрафной':
                Points['points2']['penalty'] += 3
                Points['points2']['total'] += 7
            case 'Дроп-гол':
                Points['points2']['dropgol'] += 3
                Points['points2']['total'] += 3
    else:
        match i.GolType:
            case 'Попытка':
                Points['overtime']['attempts'] += 5
                Points['overtime']['total'] += 5
            case 'Реализация':
                Points['overtime']['realization'] += 3
                Points['overtime']['total'] += 3
            case 'Штрафной':
                Points['overtime']['penalty'] += 7
                Points['overtime']['total'] += 7
            case 'Дроп-гол':
                Points['overtime']['dropgol'] += 3
                Points['overtime']['total'] += 3
    return Points

def scoreCount(id):
    gols=Gols.objects.filter(MatchID=id)
    total_gols_a,total_gols_b=0,0
    for i in gols:
        if i.PlayerID.Team == i.MatchID.TeamA:
            total_gols_a+=i.GolType.Points
        else:
            total_gols_b+=i.GolType.Points
    return {'GolsB':total_gols_b,'GolsA':total_gols_a}

def match_list(request):
    match_l=Match.objects.all()
    p={}
    for i in match_l:
        print(i.id)
        p[i.id] = scoreCount(i.id)   
    return render(request,'match.html',{'matches':match_l,"score":p})

def matchDetail(request, id):
    match=get_object_or_404(Match, id=id)
    with connection.cursor() as cursor:
        
        alerts=Aletrs.objects.filter(MatchID=id)#получение данных о предупреждениях из бзы данных
        gols=Gols.objects.filter(MatchID=id)#получение данных о голах из бзы данных
        deletes=Deletes.objects.filter(MatchID=id)#получение данных об удалениях из бзы данных
        changes=Changes.objects.filter(MatchID=id)#получение данных о заменах игроков из бзы данных
        
        total_gols_a,total_gols_b=0,0
        for i in gols:
            if i.PlayerID.Team == i.MatchID.TeamA:
                total_gols_a+=i.GolType.Points
            else:
                total_gols_b+=i.GolType.Points

    match_l=Match.objects.filter(id=id)

    return render(request, 'matchdetail.html',{'Gols':gols,
                                               'GolsB':total_gols_b,
                                               'GolsA':total_gols_a,
                                               'alerts':alerts,
                                               'Match':match_l,
                                               'Deletes':deletes,
                                               'Changes':changes,
                                               'matchid':id})

def save(request,id):
    with connection.cursor() as cursor:
    
        alerts=Aletrs.objects.filter(MatchID=id)
        gols=Gols.objects.filter(MatchID=id)
        deletes=Deletes.objects.filter(MatchID=id)
        changes=Changes.objects.filter(MatchID=id)
        
        total_gols_a,total_gols_b=0,0
        for i in gols:
            if i.PlayerID.Team == i.MatchID.TeamA:
                total_gols_a+=i.GolType.Points
            else:
                total_gols_b+=i.GolType.Points
    match_l=Match.objects.filter(id=id)
    for i in gols:

        if i.PlayerID.Team == match_l.get().TeamA:
            teamA=pointsCount(i, match_l)

        else:
            teamB=pointsCount(i, match_l)
    print(teamA,teamB)
    doc = DocxTemplate('templates/test.docx')
    context={'test':'testasdas',
             't':request,
             'Changes':changes,
             'Deletes':deletes,
             'Alerts':alerts,
             'Match':match_l,
             'gols':gols,
              'GoalA':teamA,'GoalB':teamB}
    
    doc.render(context)
    user_download_dir = os.path.expanduser('~\Downloads')
    print(user_download_dir)
    doc.save(''+user_download_dir+f'\{match_l.get().TeamA.Name} vs {match_l.get().TeamB.Name}.docx')
    return(render(request,'save.html',{"file":user_download_dir}))

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