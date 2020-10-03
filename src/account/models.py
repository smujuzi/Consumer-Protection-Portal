from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_delete
from django.dispatch import receiver


class MyAccountManager(BaseUserManager):
    def create_user(self, email, full_names, address, phone_number, image='default', role='complainant', password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not full_names:
            raise ValueError('Please tell us your full names')
        if not address:
            raise ValueError('Please provide a valid address')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            full_names=full_names.title(),
            address=address.title(),
            phone_number=phone_number
        )
        user.image = image
        user.role = role
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_names, address, phone_number, image='default', role='admin', password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            full_names=full_names.title(),
            address=address.title(),
            phone_number=phone_number
        )
        user.image = image
        user.role = role
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def upload_location(instance, filename):
    file_path = 'account/{name}/{id}-{filename}'.format(
        name=str(instance.full_names).split()[0], id=str(instance.id), filename=filename)
    return file_path


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    full_names = models.CharField(max_length=200, null=False, blank=False)
    address = models.CharField(max_length=1000, null=True, blank=True, default='Kawempe')
    phone_number = models.CharField(max_length=100, null=False, blank=False, unique=True)
    role = models.CharField(max_length=200, null=False, blank=False, default='complainant')
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, default='default')

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_names', 'address', 'phone_number']

    objects = MyAccountManager()

    def __str__(self):
        first, *middle, last = str(self.full_names).split()
        return first

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


@receiver(post_delete, sender=Account)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
