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
from django.shortcuts import redirect


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
            return HttpResponse(self.request.session['token'])
        else:
            error_message = response.text
            return HttpResponse(error_message)

        # Save the token
        

        # Return the response
        return "response"
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


