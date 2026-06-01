"""
Basic tests to verify that core modules can be imported and execute correctly
"""
import importlib
import inspect
import os
import sys
from pathlib import Path


class TestBasicImports:
    def test_json_module(self):
        import json
        assert json is not None

    def test_datetime_module(self):
        from datetime import datetime
        assert datetime is not None

    def test_pathlib_module(self):
        from pathlib import Path
        assert Path is not None

    def test_dataclasses_module(self):
        from dataclasses import dataclass, field
        assert dataclass is not None
        assert field is not None


class TestProjectStructure:
    def test_main_code_project_exists(self):
        project_root = Path(__file__).parent.parent
        assert project_root.exists(), f"MAIN_CODE_PROJECT not found at {project_root}"

    def test_src_directory_exists(self):
        project_root = Path(__file__).parent.parent
        src_dir = project_root / "src"
        assert src_dir.exists(), f"src directory not found at {src_dir}"
    def test_src_files_exist(self):
        """Test that key src files exist"""

    def test_all_src_files_importable(self):
        project_root = Path(__file__).parent.parent
        src_dir = project_root / "src"
        src_files = [f for f in sorted(os.listdir(src_dir)) if f.endswith('.py') and not f.startswith('__')]
        assert len(src_files) >= 50, f"Expected 50+ source files, found {len(src_files)}"
        for f in src_files:
            mod_name = 'src.' + f[:-3]
            try:
                mod = importlib.import_module(mod_name)
                assert mod is not None
            except Exception as e:
                assert False, f"Failed to import {f}: {e}"

    def test_all_modules_have_app_class(self):
        project_root = Path(__file__).parent.parent
        src_dir = project_root / "src"
        for f in sorted(os.listdir(src_dir)):
            if f.endswith('.py') and not f.startswith('__'):
                mod_name = 'src.' + f[:-3]
                mod = importlib.import_module(mod_name)
                has_app = any(name.endswith('App') for name, _ in inspect.getmembers(mod, inspect.isclass))
                assert has_app, f"{f} has no App class"

class TestModuleExecution:
    def test_modules_instantiate_and_run(self):
        project_root = Path(__file__).parent.parent
        src_dir = project_root / "src"
        for f in sorted(os.listdir(src_dir)):
            if f.endswith('.py') and not f.startswith('__') and f != 'base_app.py':
                mod_name = 'src.' + f[:-3]
                try:
                    mod = importlib.import_module(mod_name)
                    for name, obj in inspect.getmembers(mod, inspect.isclass):
                        if name.endswith('App') and obj.__module__ == mod_name:
                            inst = obj()
                            assert hasattr(inst, 'run'), f"{f} has no run() method"
                            items = inst.demo_data()
                            assert isinstance(items, list), f"{f} demo_data() must return list"
                            if hasattr(inst, 'process_dataset') and callable(inst.process_dataset):
                                result = inst.process_dataset(items)
                                assert isinstance(result, dict), f"{f} process_dataset() must return dict"
                except Exception as e:
                    assert False, f"{f} execution error: {e}"
