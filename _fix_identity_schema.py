import json

base = r'D:\OpenBase'
schema_path = r'D:\OpenBase\openbase-spec\identity\identity.schema.json'

with open(schema_path, 'r', encoding='utf-8') as f:
    schema = json.load(f)

# 放宽 ID 正则：允许第三段包含点号（支持语义化版本号）
schema['properties']['id']['pattern'] = '^[a-z]+\\.[a-z0-9_.-]+\\.[a-z0-9_.-]+$'

with open(schema_path, 'w', encoding='utf-8') as f:
    json.dump(schema, f, indent=2)

print('Schema fixed: ID pattern now accepts dots in namespace and name segments')
