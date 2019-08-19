from django.urls import path
from . import views

urlpatterns = [
    path('', views.loadHome, name="home"),
    path('new-alarm/', views.createAlarm, name="new-alarm"),
    path('view-alarm/', views.viewAlarm, name="view-alarm"),
]
