from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
from django.contrib import auth

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, client_id, password=None, **extra_fields):
        """
        Create and save a regular user with a client ID and password.
        """
        if not client_id:
            raise ValueError('The client ID field must be set')
        user = self.model(client_id=client_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, client_id, password=None, **extra_fields):
        """
        Create and save a regular user with a client ID and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(client_id, password, **extra_fields)

    def create_superuser(self, client_id, password=None, **extra_fields):
        """
        Create and save a superuser with a client ID and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(client_id, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()
