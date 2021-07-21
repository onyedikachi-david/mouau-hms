from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from mhms.users.forms import StudentUserForm, StudentRegisterForm, HostelApplication
from mhms.users.models import Room, Student, Hostel, Portal

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def student_register(request):
    student_user_form = StudentUserForm()
    student_reg_form = StudentRegisterForm()
    mydict = {'student_user_form': student_user_form, 'student_reg_form': student_reg_form}
    if request.method == 'POST':
        student_user_form = StudentUserForm(request.POST)
        print(student_user_form)
        student_reg_form = StudentRegisterForm(request.POST, request.FILES)
        print(student_reg_form)
        if student_user_form.is_valid() and student_reg_form.is_valid():
            user = student_user_form.save()
            user.set_password(user.password)
            user.save()
            student = student_reg_form.save(commit=False)
            student.user = user
            # student.assignedDoctorId = request.POST.get('assignedDoctorId')
            student = student.save()
        return HttpResponseRedirect('student-login')
    return render(request, 'users/signup.html', context=mydict)


def student_login(request):
    pass


def hostel_application(request):
    hostel_application_form = HostelApplication()
    mydict = {'hostel_application_form': hostel_application_form}
    if request.method == 'POST':
        hostel_application_form = HostelApplication(request.POST)
        print(hostel_application_form)
        if hostel_application_form.is_valid():
            hostel_app = hostel_application_form.save()
        return HttpResponseRedirect('application-success')
    return render(request, 'users/apply.html', context=mydict)


def admin_dashboard_view(request):
    student_count = Student.objects.all().count()
    staff_count = Portal.objects.all().count()
    total_rooms = Room.objects.all().count()
    rooms_available = Room.objects.all().filter(occupied=False).count()

    occupied_rooms = Room.objects.all().filter(occupied=True).count()
    mydict = {
        'student_count': student_count,
        'staff_count': staff_count,
        'total_rooms': total_rooms,
        'rooms_available': rooms_available,
        'occupied_rooms': occupied_rooms,
    }
    return render(request, 'hostel/index.html', context=mydict)
