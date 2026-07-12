import json
import os
from openbase_core.identity import generate_keypair

os.makedirs('config', exist_ok=True)
priv, pub = generate_keypair()
with open('config/keys.json', 'w') as f:
    json.dump({'private_key': priv, 'public_key': pub}, f, indent=2)
print('✅ Keys generated and saved to config/keys.json')
print(f'Public key: {pub[:20]}...')
