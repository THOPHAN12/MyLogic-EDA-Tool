"""
MyLogic EDA Tool - Core Module

Tổ chức các thuật toán EDA theo chức năng:
- synthesis: Logic synthesis algorithms
- optimization: Logic optimization algorithms  
- technology_mapping: Technology mapping algorithms
"""

# Core modules
# NOTE: Simulation module removed from project scope.

# Synthesis modules
from .synthesis.strash import *
from .synthesis.synthesis_flow import *

# Optimization modules
from .optimization.dce import *
from .optimization.cse import *
from .optimization.constprop import *
from .optimization.balance import *

# Technology mapping modules
from .technology_mapping.technology_mapping import *

from .utils.constants import PROJECT_VERSION, PROJECT_AUTHOR

__version__ = PROJECT_VERSION
__author__ = PROJECT_AUTHOR
