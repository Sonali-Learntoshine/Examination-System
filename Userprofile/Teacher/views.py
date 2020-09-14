from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from Student.models import Student, Message, Response, Result
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.core.mail import mail_admins, send_mail
from django.core.exceptions import PermissionDenied
from .forms import ExamForm, QuestionForm, Add_Stud
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from .models import ExamModel, Questions, Profile
from Exam_module.models import Exam, Subject
from Exam_module.forms import ExamForm
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.views import generic
from django.urls import reverse
from django.core import mail
from . import forms, models


def dashboard(request):
    return render(request, 'teacher/teacher_index.html')


def add_question(request):
    form = QuestionForm()
    exam = ExamModel.objects.all()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            ques = form.cleaned_data.get('ques')
            a = form.cleaned_data.get('a')
            b = form.cleaned_data.get('b')
            c = form.cleaned_data.get('c')
            d = form.cleaned_data.get('d')
            answer = form.cleaned_data.get('answer')

            obj = Questions(title=title, ques=ques, a=a, b=b, c=c, d=d, answer=answer)
            obj.save()
            return HttpResponse("Question saved successfully")
        else:
            return render(request, 'teacher/add_question.html', {'form': form, 'exam': exam})
    return render(request, 'teacher/add_question.html', {'form': form, 'exam': exam})


def add_exam(request):
    form = ExamForm()
    if request.method == "POST":
        form = ExamForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            added_by = form.cleaned_data.get('added_by')

            obj = ExamModel(title=title, added_by=added_by)
            obj.save()
            messages.success(request, 'Exam added successfully')
        else:
            return render(request, 'teacher/add_exam.html', {'form': form})
    return render(request, 'teacher/add_exam.html', {'form': form})


def hod_add_exam(request):
    form = ExamForm()
    if request.method == "POST":
        form = ExamForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            added_by = form.cleaned_data.get('added_by')

            obj = ExamModel(title=title, added_by=added_by)
            obj.save()
            messages.success(request, 'Exam added successfully')
        else:
            return render(request, 'teacher/hod_add_exam.html', {'form': form})
    return render(request, 'teacher/hod_add_exam.html', {'form': form})


class AddExam(LoginRequiredMixin, generic.CreateView):
    form_class = ExamForm
    template_name = 'teacher/add_exam.html'
    context_object_name = 'form'

    def get_login_url(self):
        return reverse('teacher:login')


def add_student(request):
    form = Add_Stud()
    if request.method == 'POST':
        form = Add_Stud(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            img = form.cleaned_data.get('img')
            caption = form.cleaned_data.get('caption')
            dob = form.cleaned_data.get('dob')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')

            obj = Profile(name=name, img=img, caption=caption, dob=dob, email=email, address=address, phone=phone)
            obj.save()
            return HttpResponse("Student Added successfully")
        else:
            return render(request, 'teacher/add_student.html', {'form': form})
    return render(request, 'teacher/add_student.html', {'form': form})


def view_question(request):
    context, q = {}, []
    exam = ExamModel.objects.all()
    for i in exam:
        context[i.title] = {}
        ques = {}
        for j in i.questions_set.all():
            option = []
            option.append(j.a)
            option.append(j.b)
            option.append(j.c)
            option.append(j.d)
            option.append(j.answer)
            ques[j.ques] = option
        context[i.title] = ques
    return render(request, 'teacher/view_question.html', {'context': context, 'exam': exam})


def view_exam(request):
    exam = ExamModel.objects.all()
    return render(request, 'teacher/view_exam.html', {'exam': exam})


def view_exam_question(request, id):
    exam = ExamModel.objects.get(id=id)
    return render(request, 'teacher/view_exam_question.html', {'exam': exam})


class DeleteQuestion(UserPassesTestMixin, generic.DeleteView):
    model = Questions

    def get_success_url(self):
        return self.request.GET.get('next')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def test_func(self):
        return True

    def handle_no_permission(self):
        messages.error(self.request, 'No Permission')
        raise PermissionDenied


def update_question(request, id):
    obj = Questions.objects.get(id=id)
    form = QuestionForm(request.POST or None, instance=obj)

    if form.is_valid():
        form = QuestionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "You successfully updated the question")
            # return redirect('view_exam')
    context = {'form': form,
               'error': 'The form was not updated successfully. please enter valid contents.'}
    return render(request, 'teacher/update_question.html', context)


'''
def update_question(request, id):
    ques = Questions.objects.get(id=id)
    form = QuestionForm(request.POST or None, instance=ques)
    if form.is_valid():
        form.save()
        messages.success(request, "Question Updated successfully")
        return render(request, 'view_exam_question.html')
    return render(request, 'update_question.html', {'form': form})
'''


@method_decorator(never_cache, 'dispatch')
class Registration(generic.CreateView):
    form_class = forms.FacultySignupForm
    context_object_name = 'form'
    template_name = 'teacher/signup.html'

    def get_success_url(self):
        return reverse('teacher:login')

    def form_valid(self, form):
        form.instance.is_active = False
        domain = get_current_site(self.request).domain  # gets current site domain
        print('*' * 20, '\n', domain, '\n', '*' * 20)
        msg = render_to_string('teacher/activation.html', {'profile': form.instance, 'domain': domain})
        verifier = 'Admin'
        if form.instance.designation != 'HOD':
            try:
                hod = models.Faculty.objects.get(designation='HOD', dept=form.instance.dept)
            except:
                hod = None
            if hod:
                verifier = 'HOD'
                # send_mail(subject='Faculty Signup', message='A faculty needs approval', fail_silently=True,
                #           recipient_list=[hod.email],
                #           connection=mail.get_connection(), html_message=msg, from_email=settings.EMAIL_HOST_USER)
                # messages.success(self.request,
                #                  'Account will be verified by your HOD, you will get a confirmation mail soon')
        else:
            if models.Faculty.objects.filter(groups__name='HOD', dept=form.instance.dept).exists():
                print(55)
                messages.error(self.request,
                               'A HOD is already registered in your department, kindly contact Examination Controller')
                return redirect('teacher:signup')
            else:
                mail_admins(subject='HOD Signup', message='A HOD needs approval', fail_silently=True,
                            connection=mail.get_connection(), html_message=msg)

            messages.success(self.request,
                             """Your account will be verified by %s.
                             Kindly Login after Verification.
                             You will get a confirmation Email""" % verifier)
        return super(Registration, self).form_valid(form)


@login_required(login_url='/login/')
def activate(request, *args, **kwargs):
    if request.user.groups.filter(name='HOD').exists() or request.user.is_superuser:
        user = get_object_or_404(models.Faculty, user_id=int(kwargs.get('pk')))
        user.is_active = True
        user.is_staff = True
        user.groups.add(Group.objects.get_or_create(name=user.designation)[0])
        user.save()
        user.email_user(subject='Account Approval',
                        message='Your account is approved , you can login now',
                        from_email=settings.EMAIL_HOST_USER)
        return HttpResponse('Done')
    else:
        messages.error(request, 'Superuser access Required')
        raise PermissionDenied


@never_cache
def login_view(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = models.Faculty.objects.get(username=username)
        except User.DoesNotExist:
            print('User model Not Exist')
            user = None

        if user is not None:
            if user.check_password(raw_password=password):
                if user.is_active:
                    user_id = authenticate(username=username, password=password)
                    login(request, user_id)
                    request.session.__setitem__('username', username)
                    request.session.__setitem__('role', user.designation)
                    request.session.__setitem__('image', user.profile_image.url)
                    messages.success(request, 'successfully logged in')
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('teacher:dashboard', user.user_id)
                else:
                    messages.error(request, 'Please wait for HOD to verify your Account')
                return redirect('teacher:signup')
            else:
                messages.error(request, "Password did not match. Try again")
                return redirect('teacher:login')

        else:
            try:
                user = Student.objects.get(username=username)
                messages.error(request, 'Redirected to  Student Page')
                return redirect('teacher:login')

            except User.DoesNotExist:
                messages.error(request, "User Does Not Found\nPlease Signup")
                return redirect('teacher:signup')

    else:
        if request.user.is_staff and request.user.username != 'admin':
            return redirect('teacher:dashboard', int(request.user.username))
        else:
            return render(request, 'teacher/login.html')


@never_cache
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('teacher:login')


class ProfileView(UserPassesTestMixin, generic.DetailView):
    model = models.Faculty
    template_name = 'teacher/profile-detail.html'
    context_object_name = 'profile'

    def test_func(self):
        return True if self.request.user.is_staff else False

    def handle_no_permission(self):
        messages.error(self.request, 'Access Denied Login with Faculty Account')
        return redirect('teacher:login')


class DeleteFacultyProfile(UserPassesTestMixin, generic.DeleteView):
    model = models.Faculty

    def get_success_url(self):
        return self.request.GET.get('next')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.groups.filter(name='HOD').exists()

    def handle_no_permission(self):
        messages.error(self.request, 'No Permission')
        raise PermissionDenied


class FacultyDashboard(LoginRequiredMixin, generic.DetailView):
    model = models.Faculty
    template_name = 'teacher/teacher_index.html'
    context_object_name = 'user'

    def get_login_url(self):
        return reverse('teacher:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.username != str(self.kwargs.get('pk')):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = models.Faculty.objects.get(username=self.request.user)
        context['exam'] = Exam.objects.filter(start_date__year=timezone.now().year)
        if user.dept == 'AS' and user.designation != 'HOD':
            context['subjects'] = Subject.objects.filter(sem__in=[1, 2])
            self.template_name = 'teacher/applied-science-dashboard.html'
        else:
            context['subjects'] = Subject.objects.filter(dept=user.dept)

        if user.designation == 'HOD':
            context['faculties'] = models.Faculty.objects.filter(dept=user.dept)
            if user.dept == 'AS':
                context['subjects'] = Subject.objects.filter(sem__in=[1, 2])
                context['students'] = Student.objects.filter(sem__in=[1, 2])
                self.template_name = 'teacher/applied-science-HOD.html'
            else:
                context['students'] = Student.objects.filter(dept=user.dept)
                self.template_name = 'teacher/HOD.html'

        return context


class ResponseList(UserPassesTestMixin, generic.ListView):
    template_name = 'teacher/ResponseTable.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Result.objects.filter(question_paper_id=self.kwargs.get('pk'))

    def test_func(self):
        return True if self.request.user.is_staff else False

    def handle_no_permission(self):
        messages.error(self.request, 'Access Denied Login with Faculty Account')
        return redirect('teacher:login')


class ResponseDetail(UserPassesTestMixin, generic.DetailView):
    model = Result
    template_name = 'teacher/responseDetail.html'
    context_object_name = 'response'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q_responses'] = Response.objects.filter(question_paper_id=self.kwargs.get('paper_id'),
                                                         user__username=self.kwargs.get('username'))
        return context

    def test_func(self):
        return True if self.request.user.is_staff else False

    def handle_no_permission(self):
        messages.error(self.request, 'Access Denied Login with Faculty Account')
        return redirect('teacher:login')


def ajax_query(request, *args, **kwargs):
    dept = request.GET.get('dept')
    queryset = models.Faculty.objects.filter(dept=dept)
    json = {'data': list(queryset.values_list('first_name', 'last_name', 'user_id', 'email', 'is_active', 'dept'))}
    return JsonResponse(json)
