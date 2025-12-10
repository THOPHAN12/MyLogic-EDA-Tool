"""
Yosys Integration Module

Yosys synthesis integration for MyLogic EDA Tool.
"""

from .mylogic_synthesis import MyLogicSynthesis
from .mylogic_engine import MyLogicSynthesisEngine
from .mylogic_commands import MyLogicCommands
from .combinational_synthesis import CombinationalSynthesis

__all__ = [
    'MyLogicSynthesis',
    'MyLogicSynthesisEngine', 
    'MyLogicCommands',
    'CombinationalSynthesis'
]

from constants import PROJECT_VERSION, PROJECT_AUTHOR

__version__ = PROJECT_VERSION
__author__ = PROJECT_AUTHOR
