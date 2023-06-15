"""
Database Models
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user"""
        if not email:
            raise ValueError('User Must Have Error')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new super user."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=225, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tasks(models.Model):
    """Task Class"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    estimated_time = models.DecimalField(max_digits=8, decimal_places=2,
                                         null=True, blank=True)
    spent_time = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    desc = models.TextField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    title = models.TextField(max_length=80)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    title = models.TextField(max_length=80)

    class Meta:
        unique_together = (('task', 'is_done', 'title'),)
