import random
import string

from django.db import ProgrammingError


def generate_unique_code():
    """
    Generate unique code for registration.
    """
    from apps.events.models import Registration

    try:
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))  # noqa
        if Registration.objects.filter(unique_code=code).exists():
            return generate_unique_code()
    except ProgrammingError:
        pass
    return code
