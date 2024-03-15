# ainft-py

A python version of [ainft-js](https://github.com/ainft-team/ainft-js).

## Installation

```bash
pip install ainft-py
```

## Usage
```python
import os
from ainft import Ainft

ainft = Ainft(
    private_key=os.environ.get("AINETWORK_PRIVATE_KEY"),
    api_url="https://ainft-api-dev.ainetwork.ai",
    blockchain_url="https://testnet-api.ainetwork.ai",
    chain_id=0,
)
```

## Requirements
Python version should be at least 3.8 but less than 3.12.
