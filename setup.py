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
      version=ubertool.__version__,
      description='ubertool ecological risk models',
      author='Tom Purucker',
      author_email='purucker.tom@epa.gov',
      url='https://github.com/puruckertom/ubertool',
      py_modules=['ubertool_models.base.uber_model', 'ubertool_models.sip.sip', 'ubertool_models.stir.stir',
                  'ubertool_models.rice.rice', 'ubertool_models.terrplant.terrplant',
                  'ubertool_models.iec.iec', 'ubertool_models.earthworm.earthworm']
      )
