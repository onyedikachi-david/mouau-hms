from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextChoices, Model, OneToOneField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    """Default user for MOUAU Hostel Management System."""

    class Types(TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        PORTAL = "PORTAL", "Portal"

    type = CharField(
        _("Type"), max_length=50, choices=Types.choices, default=Types.STUDENT
    )
    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


################--------- Model managers goes here --------- ####################

#############----------- Model manager --------------- #########################

class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ADMIN)


class PortalManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.PORTAL)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.STUDENT)


################---------End of Model managers --------- ####################


########### Administrator proxy model and Attributes ----------------#######################


class AdminAttributes(Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/DoctorProfilePic/", null=True, blank=True
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f"{self.user}"


class Admin(User):
    objects = AdminManager()

    @property
    def doc_details(self):
        return self.adminattributes

    class Meta:
        proxy = True

    def save(
        self,
        *args,
        **kwargs,
    ):
        if not self.pk:
            self.type = User.Types.DOCTOR
        return super().save(*args, **kwargs)


########### End of Administrator proxy model and Attributes ----------------#######################

########### Portal proxy model and Attributes ----------------#######################


class PortalAttributes(Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/PortalProfilePic/", null=True, blank=True
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f"{self.get_name()}"


class Portal(User):
    objects = PortalManager()

    @property
    def doc_details(self):
        return self.portalattributes

    class Meta:
        proxy = True

    def save(
        self,
        *args,
        **kwargs,
    ):
        if not self.pk:
            self.type = User.Types.DOCTOR
        return super().save(*args, **kwargs)


########### End of Portal proxy model and Attributes ----------------#######################


########### Hostel and Room model and ----------------###################################


class Room(models.Model):
    room_num = models.IntegerField(_("Room number"))
    occupied = models.BooleanField(_("Is the room occupied?"))
    ROOM_CONDITION = [
        ('g', 'Good'),
        ('b', 'Bad'),
        ('m', 'Maintenance')
    ]
    room_condition = models.CharField(
        _("Room condition"),
        choices=ROOM_CONDITION,
        max_length=50)
    occupants = models.ForeignKey(
        "PortalAttributes",
        verbose_name=_("Room occupants"),
        on_delete=models.CASCADE)
    ROOM_STATUS = [
        ('f', 'Full'),
        ('e', 'Empty'),
    ]
    room_status = models.CharField(
        _("Is the room full or empty"),
        max_length=50, choices=ROOM_STATUS)
    total_bed_space = models.IntegerField(
        _("Total bed spaces"), default=8)


class Hostel(models.Model):
    name = models.CharField(
        _("Hostel name"),
        max_length=50)
    portal = models.ForeignKey(
        "Portal",
        verbose_name=_("Hostel Portal"),
        on_delete=models.CASCADE)
    description = models.CharField(
        _("Brief description"),
        max_length=500)
    GENDER_CHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
    ]
    gender = models.CharField(
        _("Male or Female"),
        max_length=1,
        choices=GENDER_CHOICES)
    room = models.ForeignKey(
        Room,
        verbose_name=_("Rooms"),
        on_delete=models.CASCADE)


########### End of Hostel and Room model ----------------###################################


########### Student proxy model and Attributes ----------------#######################

class Level(models.Model):
    name = models.CharField(verbose_name="Student Level", max_length=5)


class College(models.Model):
    name = models.CharField(verbose_name="Student College", max_length=5)


class Department(models.Model):
    name = models.CharField(verbose_name="Student Department", max_length=5)


class StudentAttributes(Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    reg_num = models.CharField(verbose_name="Registration Number", max_length=100, default='MOUAU/19/78765')
    level = OneToOneField(Level, on_delete=models.CASCADE, related_name="student_level")
    college = OneToOneField(College, on_delete=models.CASCADE, related_name="student_college")
    department = OneToOneField(Department, on_delete=models.CASCADE, related_name="student_department")
    hostel_allocated = OneToOneField("Hostel", on_delete=models.CASCADE, related_name="hostel_allocated")
    room = OneToOneField("Room", on_delete=models.CASCADE, related_name="room_allocated")
    # status = models.CharField(verbose_name="Is the student verified or not", choices=)
    payment_status = models.BooleanField(verbose_name="Student payment status")
    payment_date = models.DateTimeField(auto_now_add=False)
    profile_pic = models.ImageField(
        upload_to="profile_pic/DoctorProfilePic/", null=True, blank=True
    )
    address = models.CharField(max_length=40, help_text="Home Address")
    mobile = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f"{self.user} "


class Student(User):
    objects = StudentManager()

    @property
    def doc_details(self):
        return self.portalattributes

    class Meta:
        proxy = True

    def save(
        self,
        *args,
        **kwargs,
    ):
        if not self.pk:
            self.type = User.Types.DOCTOR
        return super().save(*args, **kwargs)

########### End of Student proxy model and Attributes ----------------#######################
