from django.urls import path, include
from .views import SignUpView, MyLoginView, Tasklist, focus_task_id

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', MyLoginView.as_view(), name='login'),
    path('tasklist', Tasklist.as_view(), name='tasklist'),
    path('tasklist/<int:taskid>',focus_task_id, name='focus'),
]
