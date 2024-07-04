from django.core.exceptions import ValidationError
from django.core.files import File


def file_size(value: File):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')
