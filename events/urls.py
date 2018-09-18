from django.urls import path
from . import views

urlpattners = [
    path('',views.index, name ='agenda-events-index'),

]
