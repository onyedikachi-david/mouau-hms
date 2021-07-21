# Generated by Django 3.1.13 on 2021-07-21 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210721_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentattributes',
            name='reg_num',
            field=models.CharField(default='MOUAU/19/78765', max_length=100, verbose_name='Registration Number'),
        ),
        migrations.AlterField(
            model_name='college',
            name='name',
            field=models.CharField(max_length=5, verbose_name='Student College'),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=5, verbose_name='Student Department'),
        ),
    ]