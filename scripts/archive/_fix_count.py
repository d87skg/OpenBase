with open(r'D:\OpenBase\openbase_core\tests\event\test_models.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('assert len(EventType) == 22', 'assert len(EventType) == 23')

with open(r'D:\OpenBase\openbase_core\tests\event\test_models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed: 22 -> 23')
