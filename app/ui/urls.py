from django.urls import path, include
from .views import SignUpView, MyLoginView, Tasklist, detailtask, finishtask

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', MyLoginView.as_view(), name='login'),
    path('tasklist', Tasklist.as_view(), name='tasklist'),
    path('task/<int:pk>', detailtask.as_view(), name='detail-task'),
    path('done/<int:pk>', finishtask.as_view(), name='done-task'),
]
