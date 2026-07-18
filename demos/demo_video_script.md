# OpenBase Demo — 60 Second Video Script

## Scene 1: Problem (0-10s)
[Screen: "When an AI agent makes a ,000 trade, how do you prove what happened?"]

## Scene 2: Code (10-35s)
[Screen: Python editor]
`python
from traccia import observe

@observe
def trading_agent(task):
    return agent.run(task)

result, execution = trading_agent("BUY 1000 AAPL")
[Highlight: @observe — one line is all it takes]

Scene 3: Evidence (35-50s)
[Screen: Terminal output from Demo 2]

Timeline with 9 events

.evidence package generated

Attribution: executor + supervisor

Scene 4: Call to Action (50-60s)
[Screen: github.com/d87skg/openbase]
"Star the repo. pip install traccia. Make your agent verifiable."
