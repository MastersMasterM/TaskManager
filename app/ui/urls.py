from django.urls import path, include
from .views import SignUpView, MyLoginView, Tasklist

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', MyLoginView.as_view(), name='login'),
    path('tasklist', Tasklist.as_view(), name='tasklist')
]
