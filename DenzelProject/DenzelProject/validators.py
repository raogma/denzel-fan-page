from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from re import findall


def validate_phone_only_numbers(value):
    regex = r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$'
    res = findall(regex, value)
    if not res:
        raise ValidationError('Invalid Phone Number Format@')


@deconstructible
class MinValidator:
    def __init__(self, validator):
        self.validator = validator

    def __call__(self, value):
        if len(value) < self.validator:
            raise ValidationError(f'Value must be at least {self.validator} symbols long')


@deconstructible
class MaxValidator:
    def __init__(self, validator):
        self.validator = validator

    def __call__(self, value):
        if len(value) > self.validator:
            raise ValidationError(f'Value must be {self.validator} symbols long at most')


@deconstructible
class MaxSizeValidatorMB:
    def __init__(self, validator):
        self.validator = validator

    def __call__(self, value):
        if value.file.size > self.validator * 1024 * 1024:
            raise ValidationError(f'File too large. Size should not exceed {self.validator}MB')
