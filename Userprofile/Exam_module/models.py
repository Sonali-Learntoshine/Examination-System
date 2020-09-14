from django.utils.text import slugify
from django.urls import reverse_lazy
from django.utils import timezone
from Teacher.models import DEPT
from datetime import timedelta
from django.db import models

SEM = [
    ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')
]


class Question(models.Model):
    question = models.TextField()
    type = models.CharField(max_length=15)
    max_marks = models.PositiveIntegerField(default=0)
    a = models.CharField(max_length=30, blank=True, null=True)
    b = models.CharField(max_length=30, blank=True, null=True)
    c = models.CharField(max_length=30, blank=True, null=True)
    d = models.CharField(max_length=30, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question


class Subject(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(unique=True, max_length=10)
    slug = models.SlugField(unique=True, editable=False)
    sem = models.CharField(max_length=5, choices=SEM)
    dept = models.CharField(max_length=5, choices=DEPT)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name + ' - ' + self.code

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name + ' ' + str(self.code))
        super(Subject, self).save(*args, **kwargs)


class Exam(models.Model):
    class Meta:
        get_latest_by = 'id'

    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name + ' - ' + str(self.start_date.year)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name + ' - ' + str(self.start_date.year))
        super(Exam, self).save(*args, **kwargs)

    def get_absolute_url(self, *args, **kwargs):
        return reverse_lazy('exam-details', kwargs={'slug': self.slug})

    @property
    def status(self):
        return 'Finished' if timezone.now().date() > self.end_date else 'Not Finished'

    @property
    def is_available(self):
        return True if self.start_date <= timezone.now().date() <= self.end_date else False


class QuestionPaper(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, blank=True)
    datetime = models.DateTimeField()
    duration = models.DurationField(default=timedelta(hours=1))
    max_marks = models.IntegerField()

    def __str__(self):
        return self.exam.__str__() + ' - ' + self.subject.__str__()
