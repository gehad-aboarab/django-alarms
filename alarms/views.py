from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import Alarm
import time, json
import datetime as dt
from django.core.serializers.json import DjangoJSONEncoder
import json
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

# Function that calculates the delay until each future alarm
def calculate_delays(request):
    alarms = Alarm.objects.filter(user=request.user)
    data = {'timeouts':[]}
    for alarm in alarms:
        alarm_time = alarm.time
        alarm_date = alarm.date
        alarm_datetime = dt.datetime.combine(alarm_date, alarm_time)
        
        current_datetime = dt.datetime.fromtimestamp(time.mktime(time.localtime()))
            
        # Find the difference between the alarm date/time and the current date/time
        # and calculate the total difference number of seconds
        diff = alarm_datetime - current_datetime
        tup = divmod(diff.days * 86400 + diff.seconds, 60)
        sleep_time = tup[0]*60 + tup[1]

        # If the alarm is set for the future, the difference calculated is taken
        # into account, otherwise it is disregarded
        if sleep_time > 0:
            data['timeouts'].append(sleep_time)
    
    # Send the differences calculated in json form to the client JS function
    json_data = json.dumps(data)
    print(json_data)
    return HttpResponse(json_data)

# Function that renders and displays the alarms on the home page
@login_required
def home(request):
    context = {
        'alarms': Alarm.objects.filter(user=request.user)
    }      
    return render(request, 'alarms/home.html', context)

# Function that renders and displays the detailed view of the alarm, using the Alarm model
class AlarmDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Alarm

    def test_func(self):
        alarm = self.get_object()
        if self.request.user == alarm.user:
            return True
        return False

# Class that renders and displays the form for creating a new alarm, using the Alarm model
class AlarmCreateView(LoginRequiredMixin, CreateView):
    model = Alarm
    fields = ['name', 'date', 'time']

    # Function that ensures the user is logged in when trying to create an alarm
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Class that renders and displays the form for updating an alarm, using the Alarm model
class AlarmUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Alarm
    fields = ['name', 'date', 'time']

    # Function that ensures the user is logged in when trying to edit the alarm
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # Function that authenticates the user trying to edit the alarm info
    def test_func(self):
        alarm = self.get_object()
        if self.request.user == alarm.user:
            return True
        return False

# Class that renders and displays a confirmation for deleting an alarm, using the Alarm model
class AlarmDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Alarm
    success_url = '/'

    # Function that authenticates the user trying to delete the alarm 
    def test_func(self):
        alarm = self.get_object()
        if self.request.user == alarm.user:
            return True
        return False