from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, email, is_staff, is_superuser, role, **extra_fields):
        from apps.user.models import RoleChoice

        if not email:
            raise ValueError('unique email must be required')

        password = extra_fields.pop('password', None)
        user = self.model(
            email=email,
            is_admin=is_staff,
            is_superuser=is_superuser,
            role=role,
            **extra_fields
        )

        if user.is_admin:
            user.role = RoleChoice.ADMIN
        else:
            user.role = RoleChoice.USER

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, **extra_fields):
        return self._create_user(email, False, False, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        return self._create_user(email, True, True, **extra_fields)
