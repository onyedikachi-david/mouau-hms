# Generated by Django 3.1.13 on 2021-07-21 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5, verbose_name='Student Level')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5, verbose_name='Student Level')),
            ],
        ),
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Hostel name')),
                ('description', models.CharField(max_length=500, verbose_name='Brief description')),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1, verbose_name='Male or Female')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5, verbose_name='Student Level')),
            ],
        ),
        migrations.CreateModel(
            name='PortalAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/PortalProfilePic/')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_num', models.IntegerField(verbose_name='Room number')),
                ('occupied', models.BooleanField(verbose_name='Is the room occupied?')),
                ('room_condition', models.CharField(choices=[('g', 'Good'), ('b', 'Bad'), ('m', 'Maintenance')], max_length=50, verbose_name='Room condition')),
                ('room_status', models.CharField(choices=[('f', 'Full'), ('e', 'Empty')], max_length=50, verbose_name='Is the room full or empty')),
                ('total_bed_space', models.IntegerField(default=8, verbose_name='Total bed spaces')),
                ('occupants', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.portalattributes', verbose_name='Room occupants')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='Portal',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('STUDENT', 'Student'), ('PORTAL', 'Portal')], default='STUDENT', max_length=50, verbose_name='Type'),
        ),
        migrations.CreateModel(
            name='StudentAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.BooleanField(verbose_name='Student payment status')),
                ('payment_date', models.DateTimeField()),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/DoctorProfilePic/')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('status', models.BooleanField(default=False)),
                ('college', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_college', to='users.college')),
                ('department', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_department', to='users.department')),
                ('hostel_allocated', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hostel_allocated', to='users.hostel')),
                ('level', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_level', to='users.level')),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='room_allocated', to='users.room')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='portalattributes',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hostel',
            name='portal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.portal', verbose_name='Hostel Portal'),
        ),
        migrations.AddField(
            model_name='hostel',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.room', verbose_name='Rooms'),
        ),
        migrations.CreateModel(
            name='AdminAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/DoctorProfilePic/')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]