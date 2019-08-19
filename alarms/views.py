from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Alarm
import time, json
import datetime as dt
from playsound import playsound
from django.core.serializers.json import DjangoJSONEncoder
import json

def calculate_delays(request):
    alarms = Alarm.objects.filter(user=request.user)
    data = {'timeouts':[]}
    for alarm in alarms:
        alarm_time = alarm.time
        alarm_date = alarm.date
        alarm_datetime = dt.datetime.combine(alarm_date, alarm_time)
        
        current_datetime = dt.datetime.fromtimestamp(time.mktime(time.localtime()))
            
        diff = alarm_datetime - current_datetime
        tup = divmod(diff.days * 86400 + diff.seconds, 60)
        sleep_time = tup[0]*60 + tup[1]

        if sleep_time > 0:
            data['timeouts'].append(sleep_time)
    
    json_data = json.dumps(data)
    print(json_data)
    return HttpResponse(json_data)


@login_required
def home(request):
    context = {
        'alarms': Alarm.objects.filter(user=request.user)
    }      
    return render(request, 'alarms/home.html', context)

class AlarmDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Alarm

    def test_func(self):
        alarm = self.get_object()
        if self.request.user == alarm.user:
            return True
        return False

class AlarmCreateView(LoginRequiredMixin, CreateView):
    model = Alarm
    fields = ['name', 'date', 'time']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AlarmUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Alarm
    fields = ['name', 'date', 'time']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        alarm = self.get_object()
        if self.request.user == alarm.user:
            return True
        return False

class AlarmDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Alarm
    success_url = '/'

    def test_func(self):
        alarm = self.get_object()
        if self.request.user == alarm.user:
            return True
        return False