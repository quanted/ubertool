from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

#import different_models

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


# create package with specific modules accessible
# https://packaging.python.org/en/latest/distributing/
# run python setup.py sdist

setup(name='ubertool',
      version='0.1',
      description='ubertool ecological risk models',
      author='Tom Purucker',
      author_email='purucker.tom@epa.gov',
      url='https://github.com/puruckertom/ubertool',
      py_modules=['ubertool.base.uber_model', 'ubertool.sip.sip_exe', 'ubertool.stir.stir_exe',
                  'ubertool.rice.rice_exe', 'ubertool.terrplant.terrplant_exe',
                  'ubertool.iec.iec_exe', 'ubertool.earthworm.earthworm_exe']
      )
