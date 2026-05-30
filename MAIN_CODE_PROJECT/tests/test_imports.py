"""
Basic tests to verify that core modules can be imported
"""
import sys
from pathlib import Path


class TestBasicImports:
    """Test that basic Python modules work"""

    def test_json_module(self):
        """Test importing json module"""
        import json
        assert json is not None

    def test_datetime_module(self):
        """Test importing datetime module"""
        from datetime import datetime, timedelta
        assert datetime is not None
        assert timedelta is not None

    def test_pathlib_module(self):
        """Test importing pathlib module"""
        from pathlib import Path
        assert Path is not None

    def test_dataclasses_module(self):
        """Test importing dataclasses module"""
        from dataclasses import dataclass, field
        assert dataclass is not None
        assert field is not None


class TestProjectStructure:
    """Test that project structure is correct"""

    def test_main_code_project_exists(self):
        """Test that MAIN_CODE_PROJECT directory exists"""
        project_root = Path(__file__).parent.parent
        main_code_dir = project_root / "MAIN_CODE_PROJECT"
        assert main_code_dir.exists(
        ), f"MAIN_CODE_PROJECT not found at {main_code_dir}"

    def test_src_directory_exists(self):
        """Test that src directory exists"""
        project_root = Path(__file__).parent.parent
        src_dir = project_root / "MAIN_CODE_PROJECT" / "src"
        assert src_dir.exists(), f"src directory not found at {src_dir}"

    def test_src_files_exist(self):
        """Test that key src files exist"""
        project_root = Path(__file__).parent.parent
        src_dir = project_root / "MAIN_CODE_PROJECT" / "src"

        expected_files = [
            "banking_simulation.py",
            "cli_calculator.py",
            "contact_manager.py",
            "password_generator.py",
            "task_management.py",
        ]

        for file in expected_files:
            file_path = src_dir / file
            assert file_path.exists(
            ), f"Expected file {file} not found in src directory"


class TestSrcModuleImports:
    """Test that src modules can be imported via the path configured in conftest.py"""

    def test_all_src_modules_importable(self):
        """Import every src module to validate conftest.py sys.path injection works"""
        project_root = Path(__file__).parent.parent
        src_dir = project_root / "MAIN_CODE_PROJECT" / "src"
        src_files = [f.stem for f in sorted(src_dir.iterdir())
                     if f.suffix == '.py' and not f.name.startswith('__')]
        assert len(src_files) >= 50, f"Expected 50+ source modules, found {len(src_files)}"
        for mod_name in src_files:
            __import__('src.' + mod_name, fromlist=[''])
            mod = sys.modules.get('src.' + mod_name)
            assert mod is not None, f"Failed to import src.{mod_name}"
