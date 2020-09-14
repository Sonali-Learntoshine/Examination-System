from django.db import models


class ProfileDetail(models.Model):
    fname = models.CharField(max_length=10)
    midname = models.CharField(max_length=10, blank=True)
    lname = models.CharField(max_length=10)
    roll = models.IntegerField(unique=True)
    img = models.ImageField(upload_to='uploads')
    father_name = models.CharField(max_length=25)
    mother_name = models.CharField(max_length=25)
    sex = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=3, default='F', choices=sex)
    dob = models.DateField()
    sem = models.IntegerField()
    branches = [
        ('CSE', 'Computer Science'),
        ('CE', 'Civil'),
        ('EC', 'Electronics'),
        ('EE', 'Electrical')
    ]
    branch = models.CharField(max_length=3, default='CSE', choices=branches)
    courses = [
        ('Btech', 'Btech'),
        ('Bcom', 'Bcom'),
        ('Bsc', 'Bsc')
    ]
    course = models.CharField(max_length=5, default=None, choices=courses)
    contact = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.fname
