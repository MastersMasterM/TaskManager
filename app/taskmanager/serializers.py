"""
TaskManager and SubTask Serializer
"""
from rest_framework import serializers
from core.models import Tasks, SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    """Serializer for the sub task object"""

    class Meta:
        model = SubTask
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the task object"""

    class Meta:
        model = Tasks
        exclude = ('desc',)


class TaskDetailSerializer(TaskSerializer):
    """Serializer for task detail view."""

    sub_tasks = serializers.SerializerMethodField()
    desc = serializers.CharField()

    class Meta(TaskSerializer.Meta):
        exclude = ()

    def get_sub_tasks(self, obj)->str:
        sub_tasks = SubTask.objects.filter(task=obj)
        return SubTaskSerializer(sub_tasks, many=True).data
