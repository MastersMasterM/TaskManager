"""
UI Views
"""
import requests
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm, CustomLoginForm
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

        # Return the response
        return "response"

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class Tasklist(View):
    def get(self, request):
        u_token = self.request.session['token']

        if u_token is None:
            HttpResponse("You are Not Authenticated")
        header = {
            'Authorization': f'Token {u_token}'
        }
        u_info = requests.get('http://localhost:8000' +
                              reverse('user:me'),
                              headers=header).json()
        tasks = requests.get('http://localhost:8000' +
                             reverse('taskmanager:taskmanager-list'),
                             headers=header).json()
        for t in tasks:
            if t['due_date'] is not None:
                t['due_date'] = datetime.fromisoformat(
                    t['due_date'].replace("Z", "+00:00")
                    ).replace(tzinfo=timezone.utc)
            else:
                t['due_date'] = "Hasn't Set"
        context = {
            'tasks': tasks,
            'user_info': u_info
        }

        return render(request, 'taskmanager/task.html', context)


class detailtask(View):
    def get(self, request, pk):
        u_token = self.request.session['token']

        if u_token is None:
            HttpResponse("You are Not Authenticated")
        header = {
            'Authorization': f'Token {u_token}'
        }
        tasks = requests.get('http://localhost:8000' +
                             reverse('taskmanager:taskmanager-detail',
                                     kwargs={'pk': pk}),
                             headers=header).json()
        tasks['created_at'] = datetime.strptime(
            tasks['created_at'],
            '%Y-%m-%dT%H:%M:%S.%fZ')
        context = {
            'tasks': tasks,
            'today': date.today(),
        }

        if tasks['due_date'] is not None:
            tasks['due_date'] = datetime.strptime(
                tasks['due_date'],
                '%Y-%m-%dT%H:%M:%SZ')
            rem_days = (tasks['due_date'].date() - date.today()).days
            if rem_days < 0:
                rem_days = "The deadline is over"
        else:
            rem_days = "Due Date Hasn't Set"

        if tasks['is_done']:
            rem_days = "The task is already done"

        context['remaining'] = rem_days
        return render(request, 'taskmanager/task-detail.html', context)


class finishtask(View):
    def get(self, request, pk):
        u_token = self.request.session['token']

        if u_token is None:
            HttpResponse("You are Not Authenticated")
        header = {
            'Authorization': f'Token {u_token}',
            'Content-Type': 'application/json',
        }
        data = {'is_done': True}
        json_data = json.dumps(data)
        requests.patch('http://localhost:8000' +
                       reverse('taskmanager:taskmanager-detail',
                               kwargs={'pk': pk}),
                       headers=header,
                       data=json_data).json()
        return redirect('tasklist')


class newtask(View):
    def get(self, request):
        return render(request, 'taskmanager/new-task.html')

    def post(self, request):
        u_token = self.request.session['token']

        if u_token is None:
            HttpResponse("You are Not Authenticated")
        header = {
            'Authorization': f'Token {u_token}',
            'Content-Type': 'application/json',
        }
        print(request.POST.get('due_date'), type(request.POST.get('due_date')))
        context = {
            'title': request.POST.get('title'),
            'desc': request.POST.get('description'),
            'estimated_time': request.POST.get('estimated_time'),
            'user': self.request.session['user_id']
        }

        if request.POST.get('due_date') != '':
            context['due_date'] = datetime.strptime(
                request.POST.get('due_date'),
                '%Y-%m-%d'
                ).strftime('%Y-%m-%dT%H:%M:%S')

        json_data = json.dumps(context)
        requests.post('http://localhost:8000' +
                      reverse('taskmanager:taskmanager-list'),
                      headers=header,
                      data=json_data).json()
        return redirect('tasklist')


class welcomepage(View):
    def get(self, request):
        return render(request, 'index.html')
