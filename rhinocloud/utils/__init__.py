from django.core.validators import validate_email
import random
import string


def extract_domain(email):
    try:
        validate_email(email)
        return email.split('@')[1]
    except:
        return None

get_email_domain = extract_domain

def random_generator(base_string, max_length=30, random_string=(string.ascii_uppercase + string.digits)):
    base = base_string[:max_length]
    return '%s%s' % (base, ''.join([random.choice(random_string) for i in range(max_length - len(base))]))
