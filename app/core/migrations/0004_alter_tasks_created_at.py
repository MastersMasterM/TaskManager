# Generated by Django 4.1.9 on 2023-06-14 19:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_user_id_tasks_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 6, 14, 19, 31, 32, 547429)),
        ),
    ]