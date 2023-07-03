"""
UI Views
"""
import requests
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm,CustomLoginForm
from django.views import View
from django.shortcuts import render, redirect
from datetime import datetime, timezone, date
import json

class SignUpView(CreateView):
    template_name = 'user/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')


class MyLoginView(LoginView):
    template_name = 'user/login.html'
    form_class = CustomLoginForm

    def get_success_url(self):
        return reverse_lazy('tasks') 
    
    def form_valid(self, form):
        url = reverse('user:token')

        # Get the token from the API
        data = {
            'email': form.cleaned_data['email'],
            'password': form.cleaned_data['password']
        }
        
        response = requests.post('http://localhost:8000'+url, data=data)
        if response.status_code == 200:

            response_data = response.json()
            self.request.session['token'] = response_data['token']
            self.request.session['user_id'] = response_data['user_id']
            return redirect(reverse('tasklist'))
        else:
            error_message = response.text
            return HttpResponse(error_message)

        # Save the token
        

        # Return the response
        return "response"
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class Tasklist(View):
    def get(self, request):
        u_token = self.request.session['token']

        if u_token is None:
            HttpResponse("You are Not Authenticated")
        header = {
            'Authorization': f'Token {u_token}'
        }
        u_info = requests.get('http://localhost:8000'+reverse('user:me'), headers=header).json()
        tasks = requests.get('http://localhost:8000'+reverse('taskmanager:taskmanager-list'), headers=header).json()
        for t in tasks:
            t['due_date'] = datetime.fromisoformat(t['due_date'].replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
        context = {
            'tasks': tasks,
            'user_info': u_info
        }

        return render(request, 'taskmanager/task.html', context)


class detailtask(View):
    def get(self,request, pk):
        u_token = self.request.session['token']

        if u_token is None:
            HttpResponse("You are Not Authenticated")
        header = {
            'Authorization': f'Token {u_token}'
        }
        tasks = requests.get('http://localhost:8000'+reverse('taskmanager:taskmanager-detail', kwargs={'pk': pk}), headers=header).json()
        tasks['created_at'] = datetime.strptime(tasks['created_at'],'%Y-%m-%dT%H:%M:%S.%fZ')
        tasks['due_date'] = datetime.strptime(tasks['due_date'],'%Y-%m-%dT%H:%M:%S.%fZ')
        rem_days = (tasks['due_date'].date() - date.today()).days
        if rem_days < 0:
            rem_days = "The deadline is over"
        if tasks['is_done'] == True:
            rem_days = "The task is already done"
        context = {
            'tasks': tasks,
            'today': date.today(),
            'remaining': rem_days
        }
        return render(request, 'taskmanager/task-detail.html', context)

class finishtask(View):
    def get(self,request, pk):
        u_token = self.request.session['token']

        if u_token is None:
            HttpResponse("You are Not Authenticated")
        header = {
            'Authorization': f'Token {u_token}',
            'Content-Type': 'application/json',
        }
        data = {'is_done':True}
        json_data = json.dumps(data)
        tasks = requests.patch('http://localhost:8000'+reverse('taskmanager:taskmanager-detail', kwargs={'pk': pk}), headers=header, data=json_data).json()
        print(tasks)
        return redirect('tasklist')