"""
Test for taskmanager API
"""
from decimal import Decimal
from datetime import datetime
import pytz

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Tasks,
    SubTask
)

from taskmanager.serializers import (
    TaskSerializer,
    TaskDetailSerializer
)


TASK_URL = reverse('taskmanager:taskmanager-list')


def detail_url(taskmanager_id):
    """Create and retuen a taskmanager detail URL"""
    return reverse('taskmanager:taskmanager-detail', args=[taskmanager_id])


def create_task(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'Test Task'
    }
    defaults.update(params)

    task = Tasks.objects.create(user=user, **defaults)
    return task


def create_subtask(task, **params):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'Test Task'
    }
    defaults.update(params)

    task = SubTask.objects.create(task=task, **defaults)
    return task


class PublicTaskAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTaskAPITests(TestCase):
    """Test authenticated API request"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass1234',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_task(self):
        """Test retriving a list of task"""
        create_task(user=self.user)
        create_task(user=self.user)

        res = self.client.get(TASK_URL)

        task = Tasks.objects.all().order_by('-id')
        serializer = TaskSerializer(task, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of tasks is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password1234',
        )
        create_task(user=other_user)
        create_task(user=self.user)

        res = self.client.get(TASK_URL)

        task = Tasks.objects.filter(user=self.user)
        serializer = TaskSerializer(task, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_task_desc(self):
        """Test get task details"""
        desct = {
            'desc': 'Test Desc'
        }
        task = create_task(user=self.user, **desct)

        url = detail_url(task.id)
        res = self.client.get(url)

        serializer = TaskDetailSerializer(task)
        self.assertEqual(res.data, serializer.data)

    def test_get_sub_task(self):
        """Test get task details"""
        desct = {
            'desc': 'Test Desc'
        }
        task = create_task(user=self.user, **desct)
        create_subtask(task=task)

        url = detail_url(task.id)
        res = self.client.get(url)

        serializer = TaskDetailSerializer(task)
        self.assertEqual(res.data, serializer.data)

    def test_create_task(self):
        """Test creating a task"""
        payload = {
            'due_date': datetime.fromisoformat('2023-06-15T12:32:38.297')
            .replace(tzinfo=pytz.UTC),
            'estimated_time': Decimal('5.99'),
            'desc': 'Test Desc',
            'title': 'Title test',
            'user': self.user.id,
        }
        res = self.client.post(TASK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        task = Tasks.objects.get(id=res.data['id'])
        for k, v in payload.items():
            if k != 'user':
                self.assertEqual(getattr(task, k), v)
        self.assertEqual(task.user, self.user)
