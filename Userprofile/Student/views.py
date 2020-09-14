from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate, logout
from django.utils.encoding import force_bytes, force_text
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from .forms import StudentSignupForm, ContactForm
from django.shortcuts import render, redirect
from django.conf.urls.static import settings
from Exam_module.models import Subject, Exam
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from django.views import generic
from django.urls import reverse
from . import models


@method_decorator(never_cache, 'dispatch')
class Registration(generic.CreateView, SuccessMessageMixin):
    form_class = StudentSignupForm
    context_object_name = 'form'
    template_name = 'Student/signup.html'
    success_message = "Activation link is sent to your Email\nActivate Account before Login"

    def get_success_url(self):
        return reverse('login')

    def form_valid(self, form):
        form.instance.is_active = True
        mail_subject = 'Activate your account'
        message = render_to_string('student/confirmation_email.html', {
            'user': str(form.instance.user_id),
            'domain': get_current_site(self.request).domain,
            'uid': urlsafe_base64_encode(force_bytes(form.instance.user_id)),
            'token': account_activation_token.make_token(form.instance),
        })
        to_email = form.cleaned_data.get('email')
        # send_mail(
        #     subject=mail_subject,
        #     message='Verification',
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[to_email],
        #     html_message=message,
        # )
        # messages.success(self.request, "Activation link is sent to your Email\nActivate Account before Login")
        return super(Registration, self).form_valid(form)


@never_cache
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = models.Student.objects.get(username=uid)
    except:
        user = None
    print(account_activation_token.check_token(user, token))
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('student:login')
    else:
        return HttpResponse('Activation link is invalid!')


@never_cache
def login_view(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = models.Student.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None:
            if user.is_active:
                user_id = authenticate(username=username, password=password)
                login(request, user_id)
                request.session.set_expiry(0)
                request.session.__setitem__('image', user.profile_image.url)
                messages.success(request, 'successfully logged in')
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('student:dashboard', user.username)
            else:
                messages.error(request, 'You did not verify your email')
            return redirect('student:signup')

        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                messages.error(request, 'You did not verify your email')
            else:
                messages.error(request, "Password did not match. Try again")
            return redirect('student:login')

        except User.DoesNotExist:
            messages.error(request, "User Not found please student")
            return redirect('student:signup')

    else:
        return render(request, 'accounts/login.html')


@never_cache
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('student:login')


class ProfileView(generic.DetailView):
    model = models.Student
    template_name = 'student/profile.html'


class DeleteStudentProfile(UserPassesTestMixin, generic.DeleteView):
    model = models.Student

    def get_success_url(self):
        return self.request.GET.get('next')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.groups.filter(name='HOD').exists()

    def handle_no_permission(self):
        messages.error(self.request, 'No Permission')
        raise PermissionDenied


class StudentDashboard(LoginRequiredMixin, generic.DetailView):
    model = models.Student
    template_name = 'student/dashboard.html'

    def get_context_data(self, **kwargs):
        user = super().get_object()
        context = super().get_context_data(**kwargs)
        context['subjects'] = user.subjects.all()
        if Exam.objects.exists():
            exam = Exam.objects.latest()
            if exam.is_available:
                context['papers'] = exam.questionpaper_set.filter(subject__in=user.subjects.all())

        context['notification'] = models.Message.objects.filter(student=user, status=False)
        return context

    def post(self, *args, **kwargs):
        instance = self.get_object()
        try:
            subject = Subject.objects.get(code=self.request.POST.get('subject_code'))
            instance.subjects.add(subject)
        except Subject.DoesNotExist:
            pass
        return redirect('student:dashboard', instance.user_id)


class ResultView(UserPassesTestMixin, generic.ListView):
    model = models.Result
    context_object_name = 'result'
    template_name = 'student/result.html'

    def get_queryset(self):
        return models.Result.objects.filter(student_id=self.kwargs.get('username'), exam__slug=self.kwargs.get('exam'),
                                            out=True)

    def test_func(self):
        return True if self.kwargs.get('username') == self.request.user.username else False

    def handle_no_permission(self):
        raise PermissionDenied


class NotificationView(generic.ListView):
    model = models.Message
    template_name = 'student/notification.html'

    def get_queryset(self):
        return models.Message.objects.filter(student__username=self.request.user.username)


def about(request):
    return render(request, 'about.html')


def blog(request):
    return render(request, 'blog.html')


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank You for your valuable feedback')
        else:
            messages.error(request, 'Fill The form first')
            return redirect('Student:contact')
    return render(request, 'contact.html', {'form': form})


def index(request):
    return render(request, 'index.html')


def work(request):
    return render(request, 'work.html')


class View_user(ListView):
    model = models.Student
    template_name = 'Student/view_users.html'
    context_object_name = 'users'


def profile(request, id):
    obj = models.Student.objects.get(id=id)
    print(obj)
    return render(request, 'Student/profile.html', {'data': obj})


'''
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

            obj = models.Student(name=name, img=img, caption=caption, dob=dob, email=email, address=address, phone=phone)
            obj.save()
            return HttpResponse("Student Added successfully")
        else:
            return render(request, 'Student/add_student.html', {'form': form})
    return render(request, 'Student/add_student.html', {'form': form})


def del_student(request, id):
    obj = Profile.objects.get(id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Data deleted Successfully")
        return redirect('Student:users')
    return render(request, 'Student/delete.html', {'obj': obj})


def update(request, id):
    obj = Profile.objects.get(id=id)
    form = Add_Stud(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {'form': form}
    return render(request, 'Student/edit.html', context)
'''
