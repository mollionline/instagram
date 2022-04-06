from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_email(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError(f"{value} уже существует.", params={'value': value})
