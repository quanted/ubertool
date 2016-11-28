import sys
import os


# Add the root of the "ubertool" (git) submodule to Python PATH
# This allows the REST_UBER modules to import models from ubertool module
# E.g.: from terrplant import terrplant_exe as terrplant

ubertool_dir = os.path.dirname(__file__)
sys.path.append(ubertool_dir)
print("Added to PYTHONPATH: {}".format(ubertool_dir))
