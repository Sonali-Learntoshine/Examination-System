# Generated by Django 3.0.6 on 2020-08-12 11:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('type', models.CharField(max_length=15)),
                ('max_marks', models.PositiveIntegerField(default=0)),
                ('a', models.CharField(blank=True, max_length=30, null=True)),
                ('b', models.CharField(blank=True, max_length=30, null=True)),
                ('c', models.CharField(blank=True, max_length=30, null=True)),
                ('d', models.CharField(blank=True, max_length=30, null=True)),
                ('answer', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('sem', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')], max_length=5)),
                ('dept', models.CharField(choices=[('AS', 'Applied Science'), ('CS', 'Computer Science'), ('Civil', 'Civil Engineering'), ('EC', 'Electronics and Communication'), ('EE', 'Electrical Engineering'), ('ME', 'Mechanical Engineering')], max_length=5)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=3600))),
                ('max_marks', models.IntegerField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam_module.Exam')),
                ('questions', models.ManyToManyField(blank=True, to='Exam_module.Question')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Exam_module.Subject')),
            ],
        ),
    ]