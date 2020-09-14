from django.contrib.auth.models import User
from django.db import models

DEPT = [
    ('AS', 'Applied Science'),
    ('CS', 'Computer Science'),
    ('Civil', 'Civil Engineering'),
    ('EC', 'Electronics and Communication'),
    ('EE', 'Electrical Engineering'),
    ('ME', 'Mechanical Engineering'),
]

DESIGNATION = [
    ('Assistant Professor', 'Assistant Professor'),
    ('Professor', 'Professor'),
    ('HOD', 'HOD'),
]


class Faculty(User):
    user_id = models.BigIntegerField(primary_key=True)
    date_of_birth = models.DateField(blank=True, null=True)
    dept = models.CharField(max_length=10, choices=DEPT)
    phone = models.BigIntegerField(blank=True, null=True)
    designation = models.CharField(max_length=30, choices=DESIGNATION, default='Assistant Professor')
    profile_image = models.ImageField(upload_to='profile', blank=False, null=False)
    REQUIRED_FIELDS = ['email', 'user_id']

    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def save(self, *args, **kwargs):
        if not self.id:
            self.username = str(self.user_id)
        super().save(*args, **kwargs)


class ExamModel(models.Model):
    title = models.CharField(max_length=100, unique=True)
    added_by = models.CharField(max_length=40)
    added_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Questions(models.Model):
    title = models.ForeignKey(ExamModel, on_delete=models.CASCADE)
    ques = models.CharField(max_length=300)
    a = models.CharField(max_length=50)
    b = models.CharField(max_length=50)
    c = models.CharField(max_length=50)
    d = models.CharField(max_length=50)

    ans = [
        ("a", "a"),
        ("b", "b"),
        ("c", "c"),
        ("d", "d")
    ]

    answer = models.CharField(max_length=50, choices=ans)

    def __str__(self):
        return self.title.title + ' : ' + self.ques


class Profile(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20, unique=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=12, unique=True)
    img = models.ImageField(upload_to='uploads')
    caption = models.TextField(max_length=500)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    dob = models.DateField()

    def __str__(self):
        return self.name
