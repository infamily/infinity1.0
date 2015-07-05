# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('personal', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reason', models.TextField()),
                ('quantity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('personal', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('summary', models.CharField(max_length=150)),
                ('goal', models.ForeignKey(related_name='goal_ideas', to='core.Goal')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('http_accept_language', models.CharField(max_length=255, null=True, blank=True)),
                ('omegawiki_language_id', models.PositiveIntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Need',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('defined_meaning_id', models.PositiveIntegerField(null=True, blank=True)),
                ('definition', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=150)),
                ('language', models.ForeignKey(blank=True, to='core.Language', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('personal', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('deliverable', models.TextField()),
                ('situation', models.TextField()),
                ('idea', models.ForeignKey(related_name='idea_plans', to='core.Idea')),
                ('language', models.ForeignKey(blank=True, to='core.Language', null=True)),
                ('user', models.ForeignKey(related_name='user_plans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('personal', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('deliverables', models.CharField(max_length=150)),
                ('priority', models.IntegerField()),
                ('objective', models.TextField()),
                ('investables', models.CharField(max_length=150)),
                ('language', models.ForeignKey(blank=True, to='core.Language', null=True)),
                ('plan', models.ForeignKey(related_name='plan_steps', to='core.Plan')),
                ('user', models.ForeignKey(related_name='user_steps', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('personal', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('priority', models.IntegerField()),
                ('language', models.ForeignKey(blank=True, to='core.Language', null=True)),
                ('step', models.ForeignKey(related_name='step_tasks', to='core.Step')),
                ('user', models.ForeignKey(related_name='user_tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('personal', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=150)),
                ('url', models.URLField(max_length=150, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(null=True, upload_to=b'files', blank=True)),
                ('parent_work_id', models.PositiveIntegerField(null=True, blank=True)),
                ('description', models.TextField(blank=True)),
                ('language', models.ForeignKey(blank=True, to='core.Language', null=True)),
                ('task', models.ForeignKey(related_name='task_works', to='core.Task')),
                ('user', models.ForeignKey(related_name='user_works', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='need',
            name='type',
            field=models.ForeignKey(blank=True, to='core.Type', null=True),
        ),
        migrations.AddField(
            model_name='need',
            name='user',
            field=models.ForeignKey(related_name='user_needs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='idea',
            name='language',
            field=models.ForeignKey(blank=True, to='core.Language', null=True),
        ),
        migrations.AddField(
            model_name='idea',
            name='user',
            field=models.ForeignKey(related_name='user_ideas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='goal',
            name='language',
            field=models.ForeignKey(blank=True, to='core.Language', null=True),
        ),
        migrations.AddField(
            model_name='goal',
            name='need',
            field=models.ForeignKey(to='core.Need'),
        ),
        migrations.AddField(
            model_name='goal',
            name='user',
            field=models.ForeignKey(related_name='user_goals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='need',
            unique_together=set([('language', 'name', 'definition')]),
        ),
    ]
