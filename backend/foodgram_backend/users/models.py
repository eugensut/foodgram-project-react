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
            'unique': _('A user with that email already exists.'),
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        ordering = ['id']


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Author'
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='user_not_author'
            ),
            models.UniqueConstraint(
                fields=['following', 'user'], name='author_user'
            ),
        ]

    def __str__(self):
        return (
            f'The user {self.user} is subscribed'
            f' to the author {self.following}.'
        )
