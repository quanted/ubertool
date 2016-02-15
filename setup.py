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
      py_modules=['ubertool_models.base.uber_model', 'ubertool_models.sip.sip', 'ubertool_models.stir.stir',
                  'ubertool_models.rice.rice', 'ubertool_models.terrplant.terrplant',
                  'ubertool_models.iec.iec', 'ubertool_models.earthworm.earthworm']
      )
