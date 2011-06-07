from django.core.management.base import NoArgsCommand
from optparse import make_option
from django.contrib.auth.models import User

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
    )
    
    def handle_noargs(self, **options):
        print ', '.join([user.email for user in User.objects.all()])
