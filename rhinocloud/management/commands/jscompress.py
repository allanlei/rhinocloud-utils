from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess
import os

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-o', '--output', action='store', dest='output', help='Ouput file'),
        make_option('-d', '--directory', action='store', dest='directory', default=settings.MEDIA_ROOT, help='Directory of media files'),
        make_option('-p', '--pack', action='store_false', dest='pack', default=False, help='Pack file'),
        make_option('--defaults', action='store_true', dest='defaults', default=False, help='Generates Minified and Packed versions'),
    )
    help = 'Minifiy and/or pack Javascript'
    
    def handle(self, jsFile, output=None, directory=None, pack=False, defaults=False, *args, **kwargs):
        cmds = []
        if not directory.endswith('/'):
            directory = directory + '/'
        if not jsFile.startswith('/'):
            jsFile = '%s%s' % (directory, jsFile)
        if output is not None and not output.startswith('/'):
            jsFile = '%s%s' % (directory, output)
        
        if defaults:
            jf = jsFile.split('/')
            extension = '.' + jf[-1].split('.')[-1]
            minJS = '%s/%s' % ('/'.join(jf[:-1]), jf[-1].replace(extension, '.min%s' % extension))
            packedJS = '%s/%s' % ('/'.join(jf[:-1]), jf[-1].replace(extension, '.pack%s' % extension))
            cmds.append(['yui-compressor', jsFile, '-o', minJS, '--nomunge'])
            cmds.append(['yui-compressor', jsFile, '-o', packedJS])
        else:
            cmd = ['yui-compressor', jsFile]
            if not pack:
                cmd.append('--nomunge')
            if output is not None:
                cmd.append('-o')
                cmd.append(output)
            cmds.append(cmd)
        
        sizes = {
            'original': os.path.getsize(jsFile)
        }
        
        for cmd in cmds:
            sp = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            out = sp.communicate()[0]
            size = float(os.path.getsize(cmd[cmd.index('-o') + 1]) if '-o' in cmd else len(out))
            sizes['Minified' if '--nomunge' in cmd else 'Packed'] = size
            
        for f, size in sizes.items():
            print '%s: %s KB  (%s%%)' % (f.capitalize(), size/1024.0, size/sizes['original'] * 100.0)
