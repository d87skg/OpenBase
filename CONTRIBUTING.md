# Contributing to OpenBase

## Quick Start
`ash
pip install traccia
python
from traccia import observe

@observe
def my_agent(task):
    return f"Done: {task}"
Ways to Contribute
Add an Emitter for a new Agent framework

Improve documentation

Report bugs via Issues

Propose protocol changes via OBEP

Development
bash
git clone https://github.com/d87skg/openbase
cd openbase
pip install -e .
pytest openbase_core/tests/ -v
