with open(r'D:\OpenBase\traccia\traccia\sdk.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: agent_started only takes task string
content = content.replace("rt.agent_started(fn.__name__, task_info)", "rt.agent_started(fn.__name__)")

# Fix 2: Add tool_error to OpenBaseRuntime
with open(r'D:\OpenBase\openbase_core\registry\runtime.py', 'r', encoding='utf-8') as f:
    runtime = f.read()

old = '    def agent_failed(self, error: str) -> Event:'
new = '''    def tool_error_event(self, tool_name: str, error: str) -> Event:
        parent = self._events[-1].event_id if self._events else None
        return self.emit(self.event_factory.tool_error(tool_name, error, parent_id=parent))

    def agent_failed(self, error: str) -> Event:'''

runtime = runtime.replace(old, new)

with open(r'D:\OpenBase\openbase_core\registry\runtime.py', 'w', encoding='utf-8') as f:
    f.write(runtime)

# Fix 3: TracciaAgent calls tool_error_event instead of tool_error
content = content.replace('self._rt.tool_error(step_fn.__name__, str(e))', 'self._rt.tool_error_event(step_fn.__name__, str(e))')

with open(r'D:\OpenBase\traccia\traccia\sdk.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('API fixes applied')
