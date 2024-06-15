from django.shortcuts import get_object_or_404, redirect, render
from .models import Player,PlayerDetails,Team
from .forms import PlayerForm, TeamForm



# Create your views here.
def teams_view(request):
    team=Team.objects.filter(Trener=request.user)
    return render(request,'team.html',{'teams':team})

def player_list(request, id):
    team=Team.objects.filter(id=id)
    players=Player.objects.filter(Team_id=id)
    return render(request,'teamdetail.html',{'players':players, 'team':team})

def player_add(request,pk):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.session.get('prev_page', '/'))
    else:
        form = PlayerForm(initial={'Team':pk})
    request.session['prev_page'] = request.META.get('HTTP_REFERER', '/')
    return render(request,'playerAdd.html',{'form': form})

def edit_player(request,pk):
    player = get_object_or_404(Player, pk=pk)
    # print(mymodel_instance)
    if request.method == 'POST':
        form = PlayerForm(request.POST,instance=player)
        if form.is_valid():
            form.save()
            return redirect(request.session.get('prev_page', '/'))
    else:
        form = PlayerForm(initial={'FName':player.FName,'SName':player.SName,'LName':player.LName, 'Team':player.Team, 'Number':player.Number, 'Capitan':player.Capitan})
    request.session['prev_page'] = request.META.get('HTTP_REFERER', '/')
    return render(request,'playerAdd.html',{'form': form})

def edit_team(request,pk):
    player = get_object_or_404(Team, pk=pk)
    # print(mymodel_instance)
    if request.method == 'POST':
        form = TeamForm(request.POST,instance=player)
        if form.is_valid():
            form.save()
            return redirect(request.session.get('prev_page', '/'))
    else:
        form = TeamForm(initial={'Name':player.Name,'TShirts':player.TShirts,'Pants':player.Pants, 'City':player.City, 'Trener':request.user})
    request.session['prev_page'] = request.META.get('HTTP_REFERER', '/')
    return render(request,'playerAdd.html',{'form': form})

def delete_player(request,pk):
    player = get_object_or_404(Player, pk=pk)
    if request.method == 'POST':
        player.delete()
    return render(request,'playerAdd.html',{'form': player})

def add_team(request):
    if request.method == 'POST':
        form =TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.session.get('prev_page', '/')) 
    else:
        form = TeamForm(initial={'Trener':request.user})
    request.session['prev_page'] = request.META.get('HTTP_REFERER', '/')
    return render(request,'playerAdd.html',{'form': form})

def delete_team(request,pk):
    player = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        player.delete()
    return render(request,'playerAdd.html',{'form': player})