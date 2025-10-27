"""
AI Political Agents package for simulating historical figure debates.
"""

from .base_agent import HistoricalAgent, PersonalityTraits, HistoricalContext, Ideology
from .hitler_agent import HitlerAgent
from .gandhi_agent import GandhiAgent
from .jinnah_agent import JinnahAgent
from .churchill_agent import ChurchillAgent
from .marx_agent import MarxAgent
from .machiavelli_agent import MachiavelliAgent

__all__ = [
    'HistoricalAgent',
    'PersonalityTraits', 
    'HistoricalContext',
    'Ideology',
    'HitlerAgent',
    'GandhiAgent', 
    'JinnahAgent',
    'ChurchillAgent',
    'MarxAgent',
    'MachiavelliAgent'
]
