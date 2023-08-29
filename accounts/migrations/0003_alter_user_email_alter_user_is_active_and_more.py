# Generated by Django 4.2.3 on 2023-08-29 20:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_rename_pvmessagemodel_messagemodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                db_index=True,
                help_text="Please enter your email",
                max_length=254,
                unique=True,
                verbose_name="Email",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                db_index=True, default=True, verbose_name="Is Active"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_admin",
            field=models.BooleanField(
                db_index=True, default=False, verbose_name="Is Admin"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                db_index=True,
                help_text="Please enter your username",
                max_length=250,
                unique=True,
                verbose_name="Username",
            ),
        ),
    ]
