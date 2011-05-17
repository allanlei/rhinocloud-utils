try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import zipfile, gzip, tarfile, os

class Archive(object):
    class Meta:
        storage = None
        storage_init_params = {
            'mode': 'w'
        }
    
    def __init__(self, destination_buffer):
        self.buffer = destination_buffer
        self.storage = self.init_storage()
        if self.storage is None:
            raise Exception('No storage backend')
    
    def init_storage(self):
        return self.Meta.storage(**getattr(self.Meta, 'storage_init_params', {}))
        
    def pre_write(self, filename, string=None, fileobj=None, filepath=None):
        pass
    
    def do_write(self, filename, string=None, fileobj=None, filepath=None):
        raise NotImplementedError
        
    def post_write(self, filename, string=None, fileobj=None, filepath=None):
        pass

    def write(self, filename, string=None, fileobj=None, filepath=None):
        self.pre_write(filename=filename, string=string, fileobj=fileobj, filepath=filepath)
        self.do_write(filename=filename, string=string, fileobj=fileobj, filepath=filepath)
        self.post_write(filename=filename, string=string, fileobj=fileobj, filepath=filepath)
        
    def pre_package(self):
        pass
    
    def do_package(self):
        self.storage.close()
    
    def package(self):
        self.pre_package()
        return self.do_package()
        

class Zip(Archive):
    class Meta:
        storage = zipfile.ZipFile
        storage_init_params = {
            'mode': 'w',
            'compression': zipfile.ZIP_DEFLATED,
        }
    
    def do_write(self, filename, string=None, fileobj=None, filepath=None):
        if string:
            self.storage.writestr(filename, string)
        else:
            self.storage.write(filename, fileobj)
    
class Tar(Archive):
    class Meta:
        storage = tarfile.open
        storage_init_params = {
            'mode': 'w'
        }
    
    def init_storage(self, *args, **kwargs):
        self.Meta.storage_init_params['fileobj'] = self.buffer
        return super(Tar, self).init_storage(*args, **kwargs)
        
    def do_write(self, filename, string=None, fileobj=None, filepath=None):
        if filepath:
            self.storage.add(filepath)
        else:
            info = tarfile.TarInfo(name=filename)
            if string:
                fileobj = StringIO(string)
                info.size = len(fileobj.getvalue())
            elif fileobj:
                info.size = len(fileobj.read())
            self.storage.addfile(tarinfo=info, fileobj=fileobj)
            
class TarBz2(Tar):
    class Meta(Tar.Meta):
        storage_init_params = {
            'mode': 'w:bz2'
        }
    
class TarGz(Tar):
    class Meta(Tar.Meta):
        storage_init_params = {
            'mode': 'w:gz'
        }
