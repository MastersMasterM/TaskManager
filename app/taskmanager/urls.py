"""
URL mapping for the Taskmanager app
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from taskmanager import views


router = DefaultRouter()
router.register('taskmanager', views.TaskViewSet, 'taskmanager')
router.register('subtask', views.SubTaskViewSet, 'subtask')

app_name = 'taskmanager'

urlpatterns = [
    path('', include(router.urls)),
]
