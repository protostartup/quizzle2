# Generated by Django 2.0.4 on 2018-04-13 12:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizzes', '0012_auto_20180413_0818'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='questionstatus',
            unique_together={('student', 'question', 'quiz')},
        ),
    ]
