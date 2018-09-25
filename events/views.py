from django.shortcuts import render,get_object_or_404,redirect,render
from .models import Event,Comment
from django.utils.timezone import localdate
from django.core.paginator import Paginator,InvalidPage
from django.http import HttpResponse
from django.views.defaults import bad_request,server_error
from .forms import EventForm, CommentForm

from datetime import datetime,timedelta


ITEMS_PER_PAGE = 5
def split_date(string_date):
    """transforma a data em yyyy-mm-dd em uma tupla de tres valore para utilizar na visão de 
    eventos em um determinado dia."""
    for value in string_date.split('-'):
        yield int(value)

def index(request):

    """Exibe a pagina principal da aplicação"""

    context = {
        'hide_new_button': True,
        'priorities':Event.priorities_list,
        'today':localdate(),
    }
    return render(request,'index.html',context)

"""Exibe todos os eventos em uma página,recebe o número da página a ser visualizada via GET"""

def all(request):
    page = request. GET.get('page',1)
    paginator = Paginator(Event.objects.all(), ITEMS_PER_PAGE)
    total = paginator.count

    try:
        events = paginator.page(page)
    except InvalidPage:
        events = paginator.page(1)

    context = {
        'events':events,
        'total':total,
        'priorities':Event.priorities_list,
        'today':localdate(),
    }
    return render(request,'events.html',context)

""" Visualização dos eventos de um determinado dia, recebe a data em formato ano/mes/dia como parãmetro"""

def day(request, year:int, month:int,day:int):
    day = datetime(year,month,day)
    events = Event.objects.filter(date='{:%Y-%m-%d}'.format(day)).order_by('priority','event')
    context = {
        'today': localdate(),
        'day': day,
        'events': events,
        'next': day + timedelta(day=1),
        'previous': day - timedelta(day=1),
        'priorities': Event.priorities_list,
    }
    return render(request, 'day.html',context)

def delete(request,id:int):
     """Apaga um evento especifico, se o  movimento não existir resultará em erro 404, se
     algo errado ocorrer retornara a pagina de texto"""

     event = get_object_or_404(Event, id=id)(year,month,day)= tuple(
     split_date('{:Y-%m-%d}'.format(event.date)))
     if event.delete():
         return redirect('agenda-events-day',year=year,month=month,day=day)
     else:
         return server_error(request,'ops_500.html')

def edit(request):
    """Edita o conteudo de um evento,recebendo os dados enviados pelo
     formuário , validando e populando """

    form = EventForm(request.POST)
    if form.is_valid():
        event = get_object_or_404(Event, id=request.POST['id'])
        event.date = form.cleaned_data['date']
        event.event = form.cleaned_data['event']
        event.priority = form.cleaned_data['priority']
        event.save()
        (year , month , day) = tuple(
            split_date('{%Y-%m-%d}'.format(event.date))
        )
        return redirect('agenda-events-day',year=year,month=month,day=day)
    else:
        return bad_request(request, None, 'ops_400.html')

def new(request):
    """Recebe os dados de um novo evento via Post, faz a validação dos dados
    e ai insere na base de dados"""
    form = EventForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
        #uso a data enviada pelo formulario para o redirecionamento
        (year,month,day)=tuple(
            split_date(request.POST['date'])
        )
        return redirect('agenda-events-day', year=year, month=month, day=day)
    else:
        return bad_request(request, None , 'ops_400.html')

def show(request, id:int):
    """Visualização de um determinado evento e de seus comentários,recebe
    o 'id' do evento.Caso seja acessado via Post insere um novo comentário"""

    event = get_object_or_404(Event,id=id)
    if request.method == "POST":
        form = Comment.method(request.POST)
    if form.is_valid():
        form.save()
        return redirect('agenda-events-day', id=id)
    context ={
        'event': event,
        'comments':Comment.objects.filter(event=id).orde_by('-commented'),
        'hide_new_button':True,
        'priorities': Event.priorities_list,
        'today':localdate(),
    }
    return render(request, 'show.html',context)
