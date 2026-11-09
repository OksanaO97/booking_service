from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

def validate_name(value):
    if len(value) < 5:
        raise ValidationError(f'{value} must be more than 5')

@deconstructible
class NameValidator:
    message=' must be more than 5'

    def __call__(self, value):
        if len(value) < 5:
            raise ValidationError(value + self.message)

    def __eq__(self, other):
        return isinstance(other, NameValidator) and self.message == other.message


