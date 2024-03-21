# Generated by Django 4.2.1 on 2023-12-20 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HealthCareInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('contact', models.CharField(default='', max_length=20)),
                ('email', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=50)),
                ('city', models.CharField(default='', max_length=50)),
                ('location', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=50)),
                ('email', models.CharField(default='', max_length=50)),
                ('password', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('healthcare', models.CharField(default='', max_length=50)),
                ('name', models.CharField(default='', max_length=50)),
                ('age', models.IntegerField(default='')),
                ('address', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=50)),
                ('dose', models.IntegerField(default='')),
                ('date_selected', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('vaccine_id', models.CharField(default='', max_length=50)),
                ('type', models.CharField(default='', max_length=50)),
                ('doses', models.IntegerField(default='')),
                ('start_date', models.DateField(default='')),
                ('end_date', models.DateField(default='')),
            ],
        ),
    ]