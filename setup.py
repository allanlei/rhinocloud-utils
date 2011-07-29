from distutils.core import setup
from setuptools import find_packages
import os
import sys

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def find_packages_in(where, **kwargs):
    return [where] + ['%s.%s' % (where, package) for package in find_packages(where=where, **kwargs)]

setup(
    name = 'rhinocloud-utils',
    version = '0.1.8',
    author = 'Allan Lei',
    author_email = 'allanlei@helveticode.com',
    description = ('Django utility functions'),
    license = 'New BSD',
    keywords = 'utils django',
    url = 'https://github.com/allanlei/rhinocloud-utils',
    packages=find_packages_in('rhinocloud'),
    package_dir={'rhinocloud.contrib.jquery': 'rhinocloud/contrib/jquery'},
    package_data={'rhinocloud.contrib.jquery': ['templates/jquery/*.html']},
    long_description=read('README'),
    install_requires=[
        'gdata==2.0.14',
        'httplib2==0.6.0',      #gdata
        
        'pisa>=3.0.33',
        'html5lib==0.90',       #pisa
        'reportlab==2.5',       #pisa
        
        'wadofstuff-django-serializers>=1.1.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
