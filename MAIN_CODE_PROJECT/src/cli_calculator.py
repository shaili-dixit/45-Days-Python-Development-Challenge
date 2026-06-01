"""Build an Interactive Command-Line Calculator with Advanced Arithmetic Operations and Input Validation

Generated for the 45-day Python development challenge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple
import json
import math
import random
import time

from .base_app import BaseApp

@dataclass
class CliCalculatorAppState:
    history: List[str] = field(default_factory=list)
    records: Dict[str, Any] = field(default_factory=dict)
    flags: Dict[str, bool] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    runs: int = 0
    errors: int = 0

class CliCalculatorApp(BaseApp):
    def __init__(self) -> None:
        self.state = CliCalculatorAppState()
        self.output_dir = Path('outputs')
        self.output_dir.mkdir(exist_ok=True)

    def demo_data(self) -> List[Dict[str, Any]]:
        return [
            {'name': 'alpha', 'value': 1, 'active': True},
            {'name': 'beta', 'value': 2, 'active': False},
            {'name': 'gamma', 'value': 3, 'active': True},
        ]

    def parse_expression(self, text: str) -> Tuple[float, str, float]:
        parts = text.split()
        if len(parts) != 3:
            raise ValueError('format: number operator number')
        return float(parts[0]), parts[1], float(parts[2])

    def compute(self, a: float, op: str, b: float) -> float:
        operations = {
            '+': lambda: a + b,
            '-': lambda: a - b,
            '*': lambda: a * b,
            '/': lambda: a / b if b != 0 else math.nan,
            '%': lambda: a % b if b != 0 else math.nan,
            '**': lambda: a ** b,
        }
        if op not in operations:
            raise ValueError('unsupported operation')
        return operations[op]()

    def run(self) -> None:
        self.state.runs += 1
        samples = ['5 + 2', '8 / 0', '4 ** 3', '10 ? 2']
        self.section('Calculator Runs')
        for item in samples:
            try:
                a, op, b = self.parse_expression(item)
                result = self.compute(a, op, b)
                print(self.format_kv(item, result))
            except Exception as exc:
                self.state.errors += 1
                print(self.format_kv(item, f'error: {exc}'))
        self.display_report()
def main() -> None:
    app = CliCalculatorApp()
    try:
        app.run()
        app.finalize()
    except KeyboardInterrupt:
        print('Interrupted by user')

if __name__ == '__main__':
    main()
