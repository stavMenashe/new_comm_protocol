#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio T_PROT module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the t_prot namespace
try:
    # this might fail if the module is python-only
    from .t_prot_python import *
except ModuleNotFoundError:
    pass

# import any pure python here
from .t_modulator import t_modulator
#
