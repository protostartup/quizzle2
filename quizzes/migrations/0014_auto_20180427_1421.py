# Generated by Django 2.0.4 on 2018-04-27 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0013_auto_20180413_0822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='active',
            new_name='published',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='active',
            new_name='published',
        ),
        migrations.AddField(
            model_name='question',
            name='save_for_exam',
            field=models.BooleanField(default=False),
        ),
    ]
