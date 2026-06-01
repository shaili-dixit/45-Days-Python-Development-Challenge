"""Develop an Interactive Banking Transaction Simulation with Balance Management System

Generated for the 45-day Python development challenge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List
import json
import random
import time

from .base_app import BaseApp

@dataclass
class BankingSimulationAppState:
    history: List[str] = field(default_factory=list)
    records: Dict[str, Any] = field(default_factory=dict)
    flags: Dict[str, bool] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    runs: int = 0
    errors: int = 0

class BankingSimulationApp(BaseApp):
    def __init__(self) -> None:
        self.state = BankingSimulationAppState()
        self.output_dir = Path('outputs')
        self.output_dir.mkdir(exist_ok=True)

    def demo_data(self) -> List[Dict[str, Any]]:
        return [
            {'type': 'deposit', 'amount': 1500.0, 'timestamp': '2026-05-29T10:00:00'},
            {'type': 'withdrawal', 'amount': 200.0, 'timestamp': '2026-05-29T10:15:00'},
            {'type': 'deposit', 'amount': 350.0, 'timestamp': '2026-05-29T10:30:00'},
        ]

    def process_dataset(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        balance = 0.0
        deposits = 0
        withdrawals = 0
        amounts = []
        for tx in items:
            amount = tx.get('amount', 0.0)
            amounts.append(amount)
            if tx.get('type') == 'deposit':
                balance += amount
                deposits += 1
            elif tx.get('type') == 'withdrawal':
                balance -= amount
                withdrawals += 1
        return {
            'transaction_count': len(items),
            'final_balance': round(balance, 2),
            'deposits': deposits,
            'withdrawals': withdrawals,
            'statistics': self.summarize_list(amounts)
        }

    def deposit(self, account: Dict[str, Any], amount: float) -> Dict[str, Any]:
        if amount <= 0:
            return {'status': 'failed', 'reason': 'Negative deposit not allowed'}
        account['balance'] += amount
        tx = {'type': 'deposit', 'amount': amount, 'balance': account['balance']}
        account['transactions'].append(tx)
        return {'status': 'success', 'transaction': tx}

    def withdraw(self, account: Dict[str, Any], amount: float) -> Dict[str, Any]:
        if amount <= 0:
            return {'status': 'failed', 'reason': 'Negative withdrawal not allowed'}
        if amount > account['balance']:
            return {'status': 'failed', 'reason': 'Insufficient funds'}
        account['balance'] -= amount
        tx = {'type': 'withdrawal', 'amount': amount, 'balance': account['balance']}
        account['transactions'].append(tx)
        return {'status': 'success', 'transaction': tx}

    def get_balance(self, account: Dict[str, Any]) -> float:
        return account['balance']

    def run(self) -> None:
        self.state.runs += 1
        self.section('Banking Simulation')
        account = {'holder': 'John Doe', 'balance': 1000.0, 'transactions': []}
        print(self.format_kv('Account holder', account['holder']))
        print(self.format_kv('Opening balance', f"${account['balance']:.2f}"))
        ops = [
            ('deposit', 500),
            ('withdraw', 200),
            ('withdraw', 800),
            ('deposit', 100),
        ]
        for action, amt in ops:
            if action == 'deposit':
                result = self.deposit(account, amt)
            else:
                result = self.withdraw(account, amt)
            status = result['status']
            if status == 'success':
                tx = result['transaction']
                print(f"  {tx['type'].title():<12} ${amt:<8.2f} -> Balance: ${tx['balance']:.2f}")
            else:
                print(f"  {action.title():<12} ${amt:<8.2f} -> FAILED: {result['reason']}")
        print()
        print(self.format_kv('Final balance', f"${account['balance']:.2f}"))
        self.record('account', account)
        self.display_report()
def main() -> None:
    app = BankingSimulationApp()
    try:
        app.run()
        app.finalize()
    except KeyboardInterrupt:
        print('Interrupted by user')

if __name__ == '__main__':
    main()

