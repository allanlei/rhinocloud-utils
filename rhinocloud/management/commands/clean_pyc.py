from django.core.management.base import NoArgsCommand
from optparse import make_option
import subprocess


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--list', action='store_true', dest='list_files', default=False, help='List all pyc files to delete, but do not delete'),
    )
    help = 'Delete all pyc files'
    
    def handle_noargs(self, list_files=False, **options):
        sp = subprocess.Popen('find . -type f -name "*.pyc" -delete', shell=False, stdout=subprocess.PIPE)
        print sp.communicate()
