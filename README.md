# AI Political Agents Project

A system for simulating political debates and negotiations between AI agents modeled after historical figures with opposing ideologies.

## Research Question
Can political AI agents of historical figures who opposed each other reach a consensus in a simulated setting?

## Example Scenarios
- **Hitler vs Gandhi vs Jinnah**: Exploring ideological conflicts and potential common ground
- **US vs Japan**: Could the atomic bomb have been prevented? How?
- **Trump vs Mao**: Trade and tariff negotiations
- **Winston Churchill vs Karl Marx vs Niccolò Machiavelli**: Different political ideologies

## Key Features
- Historical figure personality modeling
- Multi-agent debate system
- Consensus detection and analysis
- Real-time negotiation simulation
- Podcast-style output generation

## Project Structure
```
├── agents/           # Historical figure AI agents
├── debates/          # Debate simulation system
├── consensus/        # Consensus detection algorithms
├── data/            # Historical data and context
├── utils/           # Utility functions
└── examples/        # Example scenarios and outputs
```

## Research Background
Based on the concept of "reposiTUm: Artificially intelligent political agents" and similar research in AI alignment and political simulation.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
from agents import HistoricalAgent
from debates import DebateSimulator

# Create agents
hitler = HistoricalAgent("Hitler", ideology="fascism")
gandhi = HistoricalAgent("Gandhi", ideology="nonviolence")
jinnah = HistoricalAgent("Jinnah", ideology="muslim_nationalism")

# Simulate debate
simulator = DebateSimulator()
result = simulator.debate([hitler, gandhi, jinnah], topic="territorial_disputes")
```

## License
MIT
# AI-UN-Repository
# aipoliagents
# aipoliagents
# aipoliagents
# aipoliagents
