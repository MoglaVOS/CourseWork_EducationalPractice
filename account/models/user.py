from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission
)


class UserManager(BaseUserManager):
    """ Manage User Model """

    def _create_user(self, email, password=None, **extra_fields):
        """Create and return a new user using an email address"""

        # Email isn't provided error handler
        if not email:
            raise AttributeError("User must set an email address")

        # Normalize email: lowercase and strip
        email = self.normalize_email(email)

        # Pass other fields
        user = self.model(email=email, **extra_fields)
        user.first_name = extra_fields.get('first_name', '')
        user.second_name = extra_fields.get('second_name', '')
        user.surname = extra_fields.get('surname', '')
        user.position = extra_fields.get('position', '')
        user.department = extra_fields.get('department', '')

        # Encrypt password
        user.set_password(password)

        # Save user data to DB
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User Model """

    # Add related_name for group and permission feedback
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

    email = models.EmailField(
        "Email Address",
        max_length=255,
        unique=True,
        help_text="Ex: example@example.com",
    )
    second_name = models.TextField("Second name", max_length=32)
    first_name = models.TextField("First name", max_length=32)
    surname = models.TextField("Surname", max_length=32, null=True, blank=True)
    position = models.TextField("Position", max_length=100)
    department = models.TextField("Department", max_length=100)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
 
    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
