from django.template.loader import render_to_string
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name ='index.html'

    
class MatchView(TemplateView):
    template_name ='match.html'

class MatchDetail(TemplateView):
    template_name='matchdetail.html'

class LoginView(TemplateView):
    template_name='login.html'


