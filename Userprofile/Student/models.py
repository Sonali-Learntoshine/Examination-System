from Exam_module.models import QuestionPaper, Question, Exam, Subject
from django.contrib.auth.models import User
from django.db import models

User._meta.get_field('email')._unique = True
User._meta.get_field('email')._blank = False
User._meta.get_field('email')._null = False

DEPT = [
    ('CS', 'Computer Science'),
    ('CE', 'Civil Engineering'),
    ('EC', 'Electronics and Communication'),
    ('EE', 'Electrical Engineering'),
    ('ME', 'Mechanical Engineering'),
]

SEM = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
]


class Student(User):
    user_id = models.BigIntegerField(primary_key=True)
    subjects = models.ManyToManyField(Subject)
    date_of_birth = models.DateField(blank=True, null=True)
    dept = models.CharField(max_length=10, choices=DEPT)
    sem = models.CharField(max_length=10, choices=SEM)
    profile_image = models.ImageField(upload_to='profile', blank=False, null=False)
    REQUIRED_FIELDS = ['email', 'roll_number', 'sem', 'year']

    @property
    def is_applied_science(self):
        return True if int(self.sem) <= 2 else False

    def save(self, *args, **kwargs):
        if not self.id:
            self.username = str(self.user_id)
        super().save(*args, **kwargs)


class Message(models.Model):
    class Meta:
        ordering = ('-id', 'status')

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.TextField(default='Result Out')
    status = models.BooleanField(default=False, editable=False)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_viewed(self):
        if not self.status:
            self.status = True
            self.save()
            return False
        else:
            return self.status


class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    viewed = models.BooleanField(default=False, editable=False)
    out = models.BooleanField(default=False, editable=False)

    @property
    def get_status(self):
        if not self.viewed:
            self.viewed = True
            self.save()
            return False
        else:
            return self.viewed

    def __str__(self):
        return str(self.student) + '-' + str(self.question_paper.exam) + '-' + str(self.question_paper)


class Response(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    gain = models.IntegerField(default=0)
    answer = models.CharField(max_length=200)


class Contact(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True)
    phone = models.IntegerField(unique=True)
    mess = models.TextField(max_length=100)

    def __str__(self):
        return self.username
