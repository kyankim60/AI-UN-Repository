"""
Main application for AI Political Agents project.
"""

import argparse
from typing import List
from agents import HitlerAgent, GandhiAgent, JinnahAgent
from debates import DebateSimulator


def create_agent(agent_name: str):
    """Create an agent by name."""
    agents = {
        "hitler": HitlerAgent,
        "gandhi": GandhiAgent,
        "jinnah": JinnahAgent,
    }
    
    if agent_name.lower() not in agents:
        raise ValueError(f"Unknown agent: {agent_name}. Available: {list(agents.keys())}")
    
    return agents[agent_name.lower()]()


def run_debate(agent_names: List[str], topic: str, max_rounds: int = 20):
    """Run a debate between specified agents."""
    
    print("=== AI Political Agents Debate ===")
    print(f"Agents: {', '.join(agent_names)}")
    print(f"Topic: {topic}")
    print("=" * 50)
    
    # Create agents
    agents = [create_agent(name) for name in agent_names]
    
    # Create debate simulator
    simulator = DebateSimulator(max_rounds=max_rounds, consensus_threshold=0.7)
    
    # Run debate
    result = simulator.debate(
        agents=agents,
        topic=topic,
        initial_context={
            "historical_period": "1940s",
            "context": "High-stakes political negotiation",
            "stakes": "Critical - involves national interests and survival"
        }
    )
    
    # Display results
    print(f"\n=== DEBATE RESULTS ===")
    print(f"Status: {result.status.value}")
    print(f"Consensus Score: {result.consensus_score:.2f}")
    print(f"Duration: {result.duration_minutes:.1f} minutes")
    print(f"Rounds: {len(result.rounds)}")
    
    print(f"\n=== KEY AGREEMENTS ===")
    for agreement in result.key_agreements:
        print(f"• {agreement}")
    
    print(f"\n=== KEY DISAGREEMENTS ===")
    for disagreement in result.key_disagreements:
        print(f"• {disagreement}")
    
    print(f"\n=== DEBATE TRANSCRIPT ===")
    print(simulator.get_debate_transcript())
    
    # Export data
    filename = f"{'_'.join(agent_names)}_{topic.replace(' ', '_')}_debate.json"
    simulator.export_debate_data(filename)
    print(f"\nDebate data exported to: {filename}")
    
    return result


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description="AI Political Agents Debate Simulator")
    parser.add_argument(
        "--agents", 
        nargs="+", 
        required=True,
        help="List of agents to include in the debate (hitler, gandhi, jinnah)"
    )
    parser.add_argument(
        "--topic", 
        required=True,
        help="Debate topic"
    )
    parser.add_argument(
        "--rounds", 
        type=int, 
        default=20,
        help="Maximum number of debate rounds"
    )
    
    args = parser.parse_args()
    
    try:
        run_debate(args.agents, args.topic, args.rounds)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
