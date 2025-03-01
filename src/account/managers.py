from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _


class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("El correo electrónico es obligatorio."))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("El superusuario debe tener is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("El superusuario debe tener is_superuser=True."))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("El superusuario debe tener is_active=True."))

        return self._create_user(email, password, **extra_fields)

    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email)
        return email.lower()
