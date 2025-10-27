"""
Base class for historical figure AI agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json


class Ideology(Enum):
    FASCISM = "fascism"
    COMMUNISM = "communism"
    CAPITALISM = "capitalism"
    NONVIOLENCE = "nonviolence"
    MUSLIM_NATIONALISM = "muslim_nationalism"
    DEMOCRACY = "democracy"
    AUTHORITARIANISM = "authoritarianism"
    LIBERALISM = "liberalism"
    CONSERVATISM = "conservatism"


@dataclass
class PersonalityTraits:
    """Core personality traits that define a historical figure's behavior."""
    assertiveness: float  # 0.0 to 1.0
    cooperativeness: float  # 0.0 to 1.0
    openness_to_change: float  # 0.0 to 1.0
    emotional_stability: float  # 0.0 to 1.0
    dominance: float  # 0.0 to 1.0
    charisma: float  # 0.0 to 1.0
    pragmatism: float  # 0.0 to 1.0
    idealism: float  # 0.0 to 1.0


@dataclass
class HistoricalContext:
    """Historical context that influences the agent's decisions."""
    time_period: str
    major_events: List[str]
    cultural_background: str
    education: str
    key_relationships: List[str]
    defining_moments: List[str]


class HistoricalAgent(ABC):
    """
    Base class for AI agents representing historical political figures.
    """
    
    def __init__(
        self,
        name: str,
        ideology: Ideology,
        personality: PersonalityTraits,
        context: HistoricalContext,
        llm_client: Any = None
    ):
        self.name = name
        self.ideology = ideology
        self.personality = personality
        self.context = context
        self.llm_client = llm_client
        self.conversation_history: List[Dict[str, Any]] = []
        self.current_position: Dict[str, Any] = {}
        self.red_lines: List[str] = []  # Non-negotiable positions
        
    @abstractmethod
    def generate_response(
        self, 
        topic: str, 
        other_agents: List['HistoricalAgent'],
        debate_context: Dict[str, Any]
    ) -> str:
        """
        Generate a response based on the agent's personality and historical context.
        """
        pass
    
    @abstractmethod
    def evaluate_proposal(
        self, 
        proposal: str, 
        proposer: 'HistoricalAgent'
    ) -> Dict[str, Any]:
        """
        Evaluate a proposal from another agent.
        Returns: {'accept': bool, 'reasoning': str, 'counter_proposal': str}
        """
        pass
    
    def update_position(self, new_position: Dict[str, Any]) -> None:
        """Update the agent's current position on the topic."""
        self.current_position.update(new_position)
    
    def add_to_history(self, speaker: str, content: str, context: Dict[str, Any]) -> None:
        """Add an interaction to the conversation history."""
        self.conversation_history.append({
            'speaker': speaker,
            'content': content,
            'context': context,
            'timestamp': len(self.conversation_history)
        })
    
    def get_personality_prompt(self) -> str:
        """Generate a personality prompt for the LLM."""
        return f"""
        You are {self.name}, a historical figure with the following characteristics:
        
        Ideology: {self.ideology.value}
        Time Period: {self.context.time_period}
        Cultural Background: {self.context.cultural_background}
        
        Personality Traits:
        - Assertiveness: {self.personality.assertiveness}
        - Cooperativeness: {self.personality.cooperativeness}
        - Openness to Change: {self.personality.openness_to_change}
        - Emotional Stability: {self.personality.emotional_stability}
        - Dominance: {self.personality.dominance}
        - Charisma: {self.personality.charisma}
        - Pragmatism: {self.personality.pragmatism}
        - Idealism: {self.personality.idealism}
        
        Key Historical Context:
        - Major Events: {', '.join(self.context.major_events)}
        - Defining Moments: {', '.join(self.context.defining_moments)}
        - Key Relationships: {', '.join(self.context.key_relationships)}
        
        Red Lines (Non-negotiable positions):
        {', '.join(self.red_lines) if self.red_lines else 'None specified'}
        
        Current Position: {json.dumps(self.current_position, indent=2)}
        
        Respond as this historical figure would, staying true to their personality,
        ideology, and historical context. Be authentic to their speaking style
        and decision-making patterns.
        """
    
    def calculate_consensus_score(self, other_agent: 'HistoricalAgent') -> float:
        """
        Calculate how likely this agent is to reach consensus with another agent.
        Returns a score between 0.0 (no consensus possible) and 1.0 (perfect alignment).
        """
        # Base compatibility on ideology similarity
        ideology_compatibility = self._calculate_ideology_compatibility(other_agent.ideology)
        
        # Factor in personality traits
        personality_compatibility = self._calculate_personality_compatibility(other_agent.personality)
        
        # Consider historical context compatibility
        context_compatibility = self._calculate_context_compatibility(other_agent.context)
        
        # Weighted average
        consensus_score = (
            ideology_compatibility * 0.4 +
            personality_compatibility * 0.3 +
            context_compatibility * 0.3
        )
        
        return min(1.0, max(0.0, consensus_score))
    
    def _calculate_ideology_compatibility(self, other_ideology: Ideology) -> float:
        """Calculate ideological compatibility between agents."""
        # Define ideology compatibility matrix
        compatibility_matrix = {
            Ideology.FASCISM: {Ideology.FASCISM: 1.0, Ideology.AUTHORITARIANISM: 0.7, Ideology.CONSERVATISM: 0.5, Ideology.COMMUNISM: 0.2, Ideology.DEMOCRACY: 0.1, Ideology.LIBERALISM: 0.1, Ideology.NONVIOLENCE: 0.0},
            Ideology.COMMUNISM: {Ideology.COMMUNISM: 1.0, Ideology.AUTHORITARIANISM: 0.6, Ideology.LIBERALISM: 0.3, Ideology.DEMOCRACY: 0.2, Ideology.CONSERVATISM: 0.2, Ideology.FASCISM: 0.2, Ideology.NONVIOLENCE: 0.1},
            Ideology.DEMOCRACY: {Ideology.DEMOCRACY: 1.0, Ideology.LIBERALISM: 0.8, Ideology.CONSERVATISM: 0.6, Ideology.NONVIOLENCE: 0.7, Ideology.COMMUNISM: 0.2, Ideology.AUTHORITARIANISM: 0.1, Ideology.FASCISM: 0.1},
            Ideology.NONVIOLENCE: {Ideology.NONVIOLENCE: 1.0, Ideology.DEMOCRACY: 0.7, Ideology.LIBERALISM: 0.6, Ideology.CONSERVATISM: 0.4, Ideology.COMMUNISM: 0.1, Ideology.AUTHORITARIANISM: 0.0, Ideology.FASCISM: 0.0},
            Ideology.MUSLIM_NATIONALISM: {Ideology.MUSLIM_NATIONALISM: 1.0, Ideology.CONSERVATISM: 0.5, Ideology.AUTHORITARIANISM: 0.4, Ideology.DEMOCRACY: 0.3, Ideology.LIBERALISM: 0.2, Ideology.COMMUNISM: 0.2, Ideology.FASCISM: 0.1, Ideology.NONVIOLENCE: 0.3},
        }
        
        return compatibility_matrix.get(self.ideology, {}).get(other_ideology, 0.5)
    
    def _calculate_personality_compatibility(self, other_personality: PersonalityTraits) -> float:
        """Calculate personality compatibility between agents."""
        # Calculate differences in key personality traits
        assertiveness_diff = abs(self.personality.assertiveness - other_personality.assertiveness)
        cooperativeness_diff = abs(self.personality.cooperativeness - other_personality.cooperativeness)
        openness_diff = abs(self.personality.openness_to_change - other_personality.openness_to_change)
        
        # Lower differences = higher compatibility
        avg_diff = (assertiveness_diff + cooperativeness_diff + openness_diff) / 3
        return 1.0 - avg_diff
    
    def _calculate_context_compatibility(self, other_context: HistoricalContext) -> float:
        """Calculate historical context compatibility between agents."""
        # Same time period = higher compatibility
        time_compatibility = 1.0 if self.context.time_period == other_context.time_period else 0.5
        
        # Shared cultural background = higher compatibility
        cultural_compatibility = 1.0 if self.context.cultural_background == other_context.cultural_background else 0.3
        
        # Shared major events = higher compatibility
        shared_events = set(self.context.major_events) & set(other_context.major_events)
        event_compatibility = len(shared_events) / max(len(self.context.major_events), len(other_context.major_events), 1)
        
        return (time_compatibility + cultural_compatibility + event_compatibility) / 3
