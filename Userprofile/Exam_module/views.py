from Student.models import Message, Response, Student, Result
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from Teacher.models import Faculty
from django.utils import timezone
from django.views import generic
from django.db.models import Q
from Exam_module import forms
from . import models


class IndexView(generic.ListView):
    model = models.Exam
    template_name = 'exam_module/index.html'
    context_object_name = 'exams'


@login_required(login_url='/student/login')
def exam_view(request, *args, **kwargs):
    question_paper = models.QuestionPaper.objects.get(id=kwargs.get('qp_id'))
    qp = question_paper.datetime
    real = timezone.now()
    if qp.timestamp() <= real.timestamp() <= (qp + question_paper.duration).timestamp():
        user = Student.objects.get(username=request.user.username)
        instance, ret = Result.objects.get_or_create(exam=question_paper.exam, question_paper=question_paper,
                                                     student=user, out=False)
        if ret:
            return render(request, 'exam_module/exam.html', {'question_paper': question_paper, 'user': user})
        else:
            return HttpResponse("Not Allowed")
    else:
        return HttpResponse("Check Time")


def saveResponse(request, *args, **kwargs):
    question_paper = models.QuestionPaper.objects.get(id=request.POST.get('paper_id'))
    if question_paper.exam.status == 'Not Finished':
        user = Student.objects.get(user_id=request.user.username)
        question = models.Question.objects.get(id=request.POST.get('question_id'))
        response = Response.objects.get_or_create(question_paper=question_paper, user=user, question=question)
        response[0].answer = request.POST.get('answer')
        response[0].save()
        return JsonResponse({'data': 'Success'})
    else:
        return JsonResponse({'data': 'Failed'})


def update_question_popup(request, *args, **kwargs):
    if request.method == 'GET':
        question = models.Question.objects.get(id=kwargs.get('pk'))
        kwargs['type'] = question.type
        form = forms.QuestionForm(question.__dict__)
    else:
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponse(
                '<script>opener.closePopup(window, "%s", "%s", "#id_question");</script>' % (instance.pk, instance))
    return render(request, 'exam_module/addQuestionForm.html', {'type': kwargs.get('type'), 'form': form})


def ajaxSubmission(request):
    res = Response.objects.get(
        user__username=request.POST.get('username'),
        question_paper_id=request.POST.get('qp_id'),
        question_id=request.POST.get('q_id'),
    )
    if int(request.POST.get('marks')) > res.question.max_marks:
        return JsonResponse({'data': 'Failed'})
    else:
        res.gain = request.POST.get('marks')
        res.save()
        return JsonResponse({'data': 'Success'})


class AddExam(LoginRequiredMixin, generic.CreateView):
    form_class = forms.ExamForm
    template_name = 'teacher/hod_add_exam.html'
    context_object_name = 'form'

    def get_login_url(self):
        return reverse('teacher:login')


class ExamDetail(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = models.Exam
    template_name = 'exam_module/ExamDetails.html'
    context_object_name = 'exam'

    def get_login_url(self):
        return reverse('teacher:login')

    def test_func(self):
        if self.request.user.is_staff:
            return True

    def handle_no_permission(self):
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usr = Faculty.objects.get(username=self.request.user.username)
        context['user'] = usr
        if usr.dept == 'AS':
            context['question_paper'] = models.QuestionPaper.objects.filter(exam__start_date__year=timezone.now().year,
                                                                            subject__sem__in=[1, 2])
            self.template_name = 'exam_module/applied-science-exam-detail.html'
        else:
            context['question_paper'] = models.QuestionPaper.objects.filter(exam__start_date__year=timezone.now().year,
                                                                            subject__dept=usr.dept)
        return context


class AddSubject(LoginRequiredMixin, generic.CreateView):
    form_class = forms.SubjectForm
    template_name = 'exam_module/SubjectForm.html'

    def get_login_url(self):
        return reverse('teacher:login')

    def get_success_url(self):
        if self.request.POST.get('next'):
            return self.request.POST.get('next')
        else:
            return reverse('teacher:dashboard', int(self.request.user.username))


class AddQuestionPaper(LoginRequiredMixin, generic.CreateView):
    form_class = forms.QuestionPaperForm
    template_name = 'exam_module/QuestionPaperForm.html'

    def get_form(self, form_class=None):
        form = super().get_form()
        form.instance.exam = models.Exam.objects.get(slug=self.kwargs.get('slug'))
        return form

    def get_login_url(self):
        return reverse('teacher:login')

    def get_success_url(self):
        return reverse('exam:exam-details', kwargs={'slug': self.kwargs.get('slug')})


class ViewQuestionPaper(LoginRequiredMixin, generic.DetailView):
    model = models.QuestionPaper
    template_name = 'exam_module/QuestionPaperDetails.html'

    def get_login_url(self):
        return reverse('teacher:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            raise PermissionDenied
        else:
            return super().dispatch(request, *args, **kwargs)


def add_question_popup(request, *args, **kwargs):
    form = forms.QuestionForm(request.POST or None)
    if form.is_valid():
        question_paper = models.QuestionPaper.objects.get(id=kwargs.get('pk'))
        instance = form.save(commit=False)
        instance.type = kwargs.get('type')
        instance.save()
        question_paper.questions.add(instance)
        question_paper.save()
        return HttpResponse(
            '<script>opener.closePopup(window);</script>')
    return render(request, 'exam_module/addQuestionForm.html', {'type': kwargs.get('type'), 'form': form})


class DeleteQuestionPaper(UserPassesTestMixin, generic.DeleteView):
    model = models.QuestionPaper

    def get_success_url(self):
        return self.request.GET.get('next')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def test_func(self):
        return True if self.request.user.is_staff else False

    def handle_no_permission(self):
        raise PermissionDenied


class EditQuestion(generic.UpdateView):
    model = models.Question
    template_name = 'exam_module/addQuestionForm.html'
    context_object_name = 'form'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('exam:exam-details', kwargs={'slug': self.kwargs.get('slug')})


class DeleteQuestion(generic.DeleteView, UserPassesTestMixin):
    model = models.Question

    def test_func(self):
        return True if self.request.user.is_staff else False

    def handle_no_permission(self):
        raise PermissionDenied

    def get(self, request, *args, **kwargs):
        self.success_url = request.GET.get('next')
        return self.post(request, *args, **kwargs)


def log_in(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'successfully logged in')
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('exam:index-page')
            else:
                messages.error(request, 'Verify your Account')
            return redirect('teacher:signup')
        else:
            messages.error(request, "Password did not match. Try again")
            return redirect('exam:login')
    else:
        return render(request, 'teacher/login.html')


def save_result(paper_id, student_id, exam_id, marks):
    paper = models.QuestionPaper.objects.get(id=paper_id)
    student = Student.objects.get(user_id=student_id)
    exam = models.Exam.objects.get(id=exam_id)
    instance, ret = Result.objects.get_or_create(exam=exam, question_paper=paper, student=student)
    instance.marks = marks
    instance.save()
    if not instance.viewed:
        text = "Response Sheet for %s - %s is checked You can check it from dashboard" % (exam.name, paper.subject.name)
        Message.objects.create(student=student, text=text, title='Response Sheet Checked')
    return instance


def question_paper_check_finish(request, *args, **kwargs):
    if request.user.is_staff:
        res_set = Response.objects.filter(
            user__username=kwargs.get('username'),
            question_paper_id=kwargs.get('paper_id'),
        )
        sm = sum([i[0] for i in res_set.values_list('gain') if i[0] is not None])
        result = save_result(paper_id=kwargs.get('paper_id'), student_id=kwargs.get('username'),
                             exam_id=kwargs.get('exam_id'), marks=sm)
        result.out = True
        result.save()
        messages.success(request, 'Saved')
        return redirect('exam:view-response-list', result.exam.slug, result.question_paper.id)
    else:
        raise PermissionDenied


def get_subject_list(request):
    keyword = request.GET.get('keyword')
    context = {
        'data': list(models.Subject.objects.filter(
            Q(name__contains=keyword) | Q(code__contains=keyword)).values('code', 'name').distinct())
    }
    return JsonResponse(context)
