# Generated by Django 4.1.9 on 2023-06-14 18:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name=datetime.datetime)),
                ('due_date', models.DateTimeField(default=None, null=True)),
                ('estimated_time', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('spent_time', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('desc', models.TextField(null=True)),
                ('is_done', models.BooleanField(default=False)),
                ('title', models.TextField(max_length=80)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_done', models.BooleanField(default=False)),
                ('title', models.TextField(max_length=80)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tasks')),
            ],
            options={
                'unique_together': {('task', 'is_done', 'title')},
            },
        ),
    ]
