from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from mhms.users.models import StudentAttributes, HostelApplicationModel

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class StudentUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["name", "email", "password", "username"]
        widgets = {"password": forms.PasswordInput()}


class StudentRegisterForm(ModelForm):
    class Meta:
        model = StudentAttributes
        fields = ["reg_num", "level", "college", "department", "address", "mobile", "profile_pic"]


class HostelApplication(ModelForm):
    class Meta:
        model = HostelApplicationModel
        fields = ["hostel", "room"]

