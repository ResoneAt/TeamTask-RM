from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class User(AbstractBaseUser):
    username = models.CharField(max_length=250, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=250, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='user', null=True, blank=True)

    job_title = models.CharField(max_length=250)
    developer = 1
    digital_marketing = 2
    business = 3
    education = 4
    personal_planning = 5
    work_field_choices = ((developer, 'Developer'),
                          (digital_marketing, 'Digital marketing'),
                          (business, 'Business'),
                          (education, 'Education'),
                          (personal_planning, 'Personal_planning'))
    work_field = models.IntegerField(choices=work_field_choices, null=True, blank=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [username]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


