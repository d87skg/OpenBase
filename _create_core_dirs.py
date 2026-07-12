import os

base = r'D:\OpenBase'
dirs = [
    'openbase-core',
    'openbase-core\event',
    'openbase-core\evidence',
    'openbase-core\replay',
    'openbase-core\trust',
    'openbase-core\certificate',
    'openbase-core\registry',
    'openbase-core\tests',
    'openbase-core\tests\event',
]

for d in dirs:
    os.makedirs(os.path.join(base, d), exist_ok=True)

# Create __init__.py files
init_files = [
    'openbase-core\__init__.py',
    'openbase-core\event\__init__.py',
    'openbase-core\evidence\__init__.py',
    'openbase-core\replay\__init__.py',
    'openbase-core\trust\__init__.py',
    'openbase-core\certificate\__init__.py',
    'openbase-core\registry\__init__.py',
    'openbase-core\tests\__init__.py',
    'openbase-core\tests\event\__init__.py',
]

for f in init_files:
    path = os.path.join(base, f)
    with open(path, 'w') as fh:
        fh.write('')
    print(f'Created: {f}')

print('Directory structure created')
