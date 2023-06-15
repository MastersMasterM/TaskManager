"""
Views for the TaskManager APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tasks, SubTask
from taskmanager import serializers


class TaskViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.TaskDetailSerializer
    queryset = Tasks.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.TaskSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)


class SubTaskViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.SubTaskSerializer
    queryset = SubTask.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
