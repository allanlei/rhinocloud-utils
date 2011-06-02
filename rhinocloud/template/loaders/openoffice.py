from django.template.loaders import app_directories, filesystem
from django.template.base import TemplateDoesNotExist
from django.template.loader import make_origin
from django.conf import settings

from rhinocloud.template.openoffice import OpenOfficeTemplate
import zipfile


def read_openoffice(filepath):
    files = zipfile.ZipFile(filepath, 'r')
    try:
        return files.read('content.xml')
    finally:
        files.close()
    
class AppDirectoriesLoader(app_directories.Loader):
    def load_template_source(self, template_name, template_dirs=None):
        for filepath in self.get_template_sources(template_name, template_dirs):
            if zipfile.is_zipfile(filepath):
                pass
            
            try:
                file = open(filepath)
                try:
                    return (file.read().decode(settings.FILE_CHARSET), filepath)
                finally:
                    file.close()
            except IOError:
                pass
        raise TemplateDoesNotExist(template_name)
        
        
class FileSystemLoader(filesystem.Loader):
    def load_template_source(self, template_name, template_dirs=None):
        tried = []
        for filepath in self.get_template_sources(template_name, template_dirs):
            if zipfile.is_zipfile(filepath):
                try:
                    return (read_openoffice(filepath), filepath)
                finally:
                    files.close()
                tried.append(filepath)
        if tried:
            error_msg = "Tried %s" % tried
        else:
            error_msg = "Your TEMPLATE_DIRS setting is empty. Change it to point to at least one template directory."
        raise TemplateDoesNotExist(error_msg)
        
    def load_template(self, template_name, template_dirs=None):
        source, display_name = self.load_template_source(template_name, template_dirs)
        origin = make_origin(display_name, self.load_template_source, template_name, template_dirs)
        try:
            return OpenOfficeTemplate(source, origin, filepath=display_name), None
        except TemplateDoesNotExist:
            # If compiling the template we found raises TemplateDoesNotExist, back off to
            # returning the source and display name for the template we were asked to load.
            # This allows for correct identification (later) of the actual template that does
            # not exist.
            return source, display_name
