# Generated by Django 4.2.3 on 2023-08-02 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is Deleted')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Deleted at')),
                ('username', models.CharField(help_text='Please enter your username', max_length=250, unique=True, verbose_name='Username')),
                ('email', models.EmailField(help_text='Please enter your email', max_length=254, unique=True, verbose_name='Email')),
                ('full_name', models.CharField(blank=True, help_text='Please enter your full name', max_length=250, null=True, verbose_name='Full name')),
                ('bio', models.TextField(blank=True, help_text='Please write about yourself', null=True, verbose_name='Bio')),
                ('image', models.ImageField(blank=True, help_text='Please upload your image.', null=True, upload_to='user', verbose_name='Image')),
                ('job_title', models.CharField(blank=True, help_text='Please enter your job title', max_length=250, null=True, verbose_name='Job title')),
                ('work_field', models.IntegerField(blank=True, choices=[(1, 'Developer'), (2, 'Digital marketing'), (3, 'Business'), (4, 'Education'), (5, 'Personal_planning')], help_text='Please enter your work field', null=True, verbose_name='Work field')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is Admin')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='PvMessageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is Deleted')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Deleted at')),
                ('text', models.TextField(help_text='Please Write Your Message')),
                ('is_read', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pv_sender', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receiver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'db_table': 'PrivateMessage',
            },
        ),
        migrations.CreateModel(
            name='NotificationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is Deleted')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Deleted at')),
                ('body', models.TextField()),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'db_table': 'Notification',
            },
        ),
    ]