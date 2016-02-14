from distutils.core import setup

# create package with specific modules accessible
# https://packaging.python.org/en/latest/distributing/
# run python setup.py sdist

setup(name='ubertool',
      version='1.0',
      description='ubertool ecological risk models',
      author='Tom Purucker',
      author_email='purucker.tom@epa.gov',
      url='https://github.com/puruckertom/ubertool',
      py_modules=['ubertool.base.uber_model', 'ubertool.sip.sip', 'ubertool.stir.stir',
                  'ubertool.rice.rice', 'ubertool.terrplant.terrplant',
                  'ubertool.iec.iec', 'ubertool.earthworm.earthworm']
      )
