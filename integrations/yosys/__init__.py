"""
Yosys Integration Module

Yosys synthesis integration for MyLogic EDA Tool.
"""

from .mylogic_synthesis import MyLogicSynthesis
from .mylogic_engine import MyLogicSynthesisEngine
from .mylogic_commands import MyLogicCommands
from .combinational_synthesis import CombinationalSynthesizer

__all__ = [
    'MyLogicSynthesis',
    'MyLogicSynthesisEngine', 
    'MyLogicCommands',
    'CombinationalSynthesizer'
]

from constants import PROJECT_VERSION, PROJECT_AUTHOR

__version__ = PROJECT_VERSION
__author__ = PROJECT_AUTHOR
