import os

code = '''"""
Tests for OpenBase CLI
"""
import sys
import os
import tempfile
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
from openbase_core.cli.main import cmd_init, cmd_status


class TestCLIInit:
    def test_init_creates_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Create a mock args
            class Args:
                dir = tmp
            cmd_init(Args())

            config_path = os.path.join(tmp, '.openbase', 'config.json')
            assert os.path.exists(config_path)

            with open(config_path, 'r') as f:
                config = json.load(f)
            assert config['version'] == '2.0.0'
            assert 'agent_id' in config

    def test_init_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            class Args:
                dir = tmp
            cmd_init(Args())

            assert os.path.exists(os.path.join(tmp, '.openbase', 'evidence'))
            assert os.path.exists(os.path.join(tmp, '.openbase', 'certificates'))

    def test_init_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            class Args:
                dir = tmp
            cmd_init(Args())
            # Second init should not crash
            cmd_init(Args())


class TestCLIStatus:
    def test_status_on_uninitialized(self):
        import io
        old_dir = os.getcwd()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                os.chdir(tmp)
                # Just verify it doesn't crash
                try:
                    cmd_status(None)
                except Exception as e:
                    pytest.fail(f"cmd_status crashed: {e}")
        finally:
            os.chdir(old_dir)
'''

path = r'D:\OpenBase\openbase_core\tests\test_cli.py'
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('test_cli.py written')
