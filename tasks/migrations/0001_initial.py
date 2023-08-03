# Generated by Django 4.2.3 on 2023-08-02 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is Deleted')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Deleted at')),
                ('title', models.CharField(help_text='Enter Board title', max_length=100, verbose_name='Title')),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('visibility', models.CharField(choices=[('public', 'Public'), ('privet', 'Privet'), ('workspace', 'Workspace')], default='workspace', max_length=20)),
                ('background', models.ImageField(blank=True, null=True, upload_to='tasks')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Board',
                'verbose_name_plural': 'Boards',
                'db_table': 'Board',
            },
        ),
        migrations.CreateModel(
            name='CardModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is Deleted')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Deleted at')),
                ('title', models.CharField(help_text='Enter Card title', max_length=150, verbose_name='Title')),
                ('description', models.TextField(blank=True, help_text="Enter card's description", null=True, verbose_name='Description')),
                ('start_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Start Time')),
                ('due_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Due Time')),
                ('reminder_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Reminder Time')),
                ('has_reminder', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('todo', 'Todo'), ('doing', 'Doing'), ('done', 'Done'), ('suspended', 'Suspended')], default='todo', max_length=20)),
                ('background_img', models.ImageField(blank=True, null=True, upload_to='tasks')),
            ],
            options={
                'verbose_name': 'Card',
                'verbose_name_plural': 'Cards',
                'db_table': 'Card',
            },
        ),
        migrations.CreateModel(
            name='WorkSpaceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is Deleted')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Deleted at')),
                ('title', models.CharField(help_text='Enter WorkSpace title', max_length=100, verbose_name='Title')),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('background', models.ImageField(blank=True, null=True, upload_to='tasks')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'WorkSpace',
                'verbose_name_plural': 'WorkSpaces',
                'db_table': 'WorkSpace',
            },
        ),
        migrations.CreateModel(
            name='WSMembershipModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('permission', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tasks.workspacemodel')),
            ],
            options={
                'verbose_name': 'Membership in Workspace',
                'verbose_name_plural': 'Workspace Memberships',
                'db_table': 'WorkspaceMembership',
            },
        ),
        migrations.CreateModel(
            name='SubTaskModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Please enter your sub task title', max_length=250, verbose_name='Title')),
                ('status', models.BooleanField(default=False, help_text='Sub Task status', verbose_name='Status')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tasks.cardmodel')),
            ],
            options={
                'verbose_name': 'SubTask',
                'verbose_name_plural': 'SubTasks',
                'db_table': 'SubTask',
            },
        ),
        migrations.CreateModel(
            name='ListModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is Deleted')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Deleted at')),
                ('title', models.CharField(help_text='Enter List title', max_length=100, verbose_name='Title')),
                ('background_color', models.CharField(blank=True, choices=[('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('orange', 'Orange'), ('purple', 'Purple'), ('yellow', 'Yellow')], max_length=10, null=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='lists', to='tasks.boardmodel')),
            ],
            options={
                'verbose_name': 'List',
                'verbose_name_plural': 'Lists',
                'db_table': 'List',
            },
        ),
        migrations.CreateModel(
            name='LabelModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter Label title', max_length=50, verbose_name='Title')),
                ('background_color', models.CharField(blank=True, choices=[('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('orange', 'Orange'), ('purple', 'Purple'), ('yellow', 'Yellow')], max_length=10, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='labels', to='tasks.cardmodel')),
            ],
            options={
                'verbose_name': 'Label',
                'verbose_name_plural': 'Labels',
                'db_table': 'Label',
            },
        ),
        migrations.CreateModel(
            name='GMessageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is Deleted')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Deleted at')),
                ('text', models.TextField(help_text='Please Write Your Message')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tasks.boardmodel')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='g_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'GMessage',
                'verbose_name_plural': 'GMessages',
                'db_table': 'GroupMessage',
            },
        ),
        migrations.CreateModel(
            name='CMembershipModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tasks.cardmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Membership in Card',
                'verbose_name_plural': 'Card Memberships',
                'db_table': 'CardMembership',
            },
        ),
        migrations.AddField(
            model_name='cardmodel',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cards', to='tasks.listmodel'),
        ),
        migrations.CreateModel(
            name='CardCommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('body', models.TextField(help_text='comment on card', verbose_name='Body')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tasks.cardmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'db_table': 'CardComment',
            },
        ),
        migrations.AddField(
            model_name='boardmodel',
            name='workspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='boards', to='tasks.workspacemodel'),
        ),
        migrations.CreateModel(
            name='BMembershipModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('permission', models.CharField(max_length=255)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tasks.boardmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Membership in Board',
                'verbose_name_plural': 'Board Memberships',
                'db_table': 'BoardMembership',
            },
        ),
    ]