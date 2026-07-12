import os

base = r'D:\OpenBase'
dirs = [
    'openclaw',
    'openclaw\runtime',
    'openclaw\agent',
    'openclaw\tools',
    'openclaw\tests',
]

for d in dirs:
    os.makedirs(os.path.join(base, d), exist_ok=True)

init_files = [
    'openclaw\__init__.py',
    'openclaw\runtime\__init__.py',
    'openclaw\agent\__init__.py',
    'openclaw\tools\__init__.py',
    'openclaw\tests\__init__.py',
]

for f in init_files:
    path = os.path.join(base, f)
    with open(path, 'w') as fh:
        fh.write('')
    print(f'Created: {f}')

print('OpenClaw directory structure created')
