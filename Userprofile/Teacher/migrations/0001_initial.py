# Generated by Django 3.0.6 on 2020-08-12 11:49

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0015_auto_20200812_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('added_by', models.CharField(max_length=40)),
                ('added_on', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('dept', models.CharField(choices=[('AS', 'Applied Science'), ('CS', 'Computer Science'), ('Civil', 'Civil Engineering'), ('EC', 'Electronics and Communication'), ('EE', 'Electrical Engineering'), ('ME', 'Mechanical Engineering')], max_length=10)),
                ('phone', models.BigIntegerField(blank=True, null=True)),
                ('designation', models.CharField(choices=[('Assistant Professor', 'Assistant Professor'), ('Professor', 'Professor'), ('HOD', 'HOD')], default='Assistant Professor', max_length=30)),
                ('profile_image', models.ImageField(upload_to='profile')),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=20, unique=True)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=12, unique=True)),
                ('img', models.ImageField(upload_to='uploads')),
                ('caption', models.TextField(max_length=500)),
                ('time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('dob', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ques', models.CharField(max_length=300)),
                ('a', models.CharField(max_length=50)),
                ('b', models.CharField(max_length=50)),
                ('c', models.CharField(max_length=50)),
                ('d', models.CharField(max_length=50)),
                ('answer', models.CharField(choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')], max_length=50)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Teacher.ExamModel')),
            ],
        ),
    ]
