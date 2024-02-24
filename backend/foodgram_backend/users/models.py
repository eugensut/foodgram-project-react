from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='username',
        help_text=(
            'Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only. Not "me"'
        ),
        validators=[
            RegexValidator(
                regex=r'^(?!me$)[\w.@+-]+\Z',
                message=(
                    'Enter a valid username. '
                    'This value may contain only letters, '
                    'numbers, @/./+/-/_ characters, and not "me". '
                )
            )
        ],
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=False,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    class Meta:
        ordering = ['id']

    @property
    def is_subscribed(self):
        return False
