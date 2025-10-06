"""
MyLogic EDA Tool - Core Module

Tổ chức các thuật toán EDA theo chức năng:
- synthesis: Logic synthesis algorithms
- optimization: Logic optimization algorithms  
- technology_mapping: Technology mapping algorithms
- vlsi_cad: VLSI CAD algorithms
"""

# Core modules
from .simulation.arithmetic_simulation import *

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

# VLSI CAD modules
from .vlsi_cad.bdd import *
from .vlsi_cad.sat_solver import *
from .vlsi_cad.placement import *
from .vlsi_cad.routing import *
from .vlsi_cad.timing_analysis import *

__version__ = "1.0.0"
__author__ = "MyLogic EDA Tool Team"
