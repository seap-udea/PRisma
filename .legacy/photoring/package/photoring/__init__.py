from photoring.version import *
import os
import warnings
import sys

################################################################################
# Directories
################################################################################
#Root directory
try:
    FILE=__file__
    ROOTDIR=os.path.abspath(os.path.dirname(FILE))
except:
    FILE=""
    ROOTDIR=os.path.abspath('')

DATA_DIR = os.path.join(ROOTDIR, 'data/').replace('//','/')

PRDATA_DIR = 'prdata/'
if os.path.exists(PRDATA_DIR) is False:
    os.makedirs(PRDATA_DIR)

PRFIG_DIR = f"{PRDATA_DIR}/figures/".replace('//','/')
if os.path.exists(PRFIG_DIR) is False:
    os.makedirs(PRFIG_DIR)

################################################################################
# Inputs
################################################################################
opts = dict()
for arg in sys.argv[1:]:
    if '=' in arg:
        key,val = arg.split('=')
        opts[key] = val

def check_opts(key,default=None):
    if key in opts.keys():
        return opts[key]
    else:
        if default is not None:
            return default
        else:
            return None

def get_ipython():
    class foo:
        def run_line_magic(self,*args):
            pass
    return foo

################################################################################
# Automatic imports
################################################################################
from photoring.geotrans import *
from photoring.montecarlo import *
from photoring.plot import *
from photoring.photoring import *

################################################################################
# Configuration
################################################################################
print(f"Photoring version {version}")
warnings.filterwarnings('ignore')
