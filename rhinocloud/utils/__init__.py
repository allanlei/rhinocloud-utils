from django.core.validators import validate_email

def extract_domain(email):
    try:
        validate_email(email)
        return email.split('@')[1]
    except:
        return None

get_email_domain = extract_domain
