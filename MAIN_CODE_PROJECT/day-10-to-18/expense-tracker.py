"""
Personal Expense Tracker with Budget Warnings and Monthly Summary Export
Tracks expenses by category/date, warns on budget overrun, exports monthly report.
"""

import json
import os
from datetime import datetime, date
from collections import defaultdict

DATA_FILE = "expenses.json"

CATEGORIES = [
    "Food", "Transport", "Entertainment", "Utilities",
    "Healthcare", "Shopping", "Education", "Rent", "Other"
]

DEFAULT_BUDGETS = {
    "Food": 5000, "Transport": 2000, "Entertainment": 1500,
    "Utilities": 3000, "Healthcare": 2000, "Shopping": 3000,
    "Education": 2000, "Rent": 12000, "Other": 1000
}


class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.budgets = dict(DEFAULT_BUDGETS)
        self._next_id = 1
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE) as f:
                    data = json.load(f)
                    self.expenses = data.get('expenses', [])
                    self.budgets = data.get('budgets', DEFAULT_BUDGETS)
                    self._next_id = max((e['id'] for e in self.expenses), default=0) + 1
            except:
                pass

    def save(self):
        with open(DATA_FILE, 'w') as f:
            json.dump({'expenses': self.expenses, 'budgets': self.budgets}, f, indent=2)

    def add(self, amount, category, description="", exp_date=None):
        if amount <= 0:
            print("  ✗ Amount must be positive.")
            return
        if category not in CATEGORIES:
            print(f"  ✗ Unknown category. Valid: {CATEGORIES}")
            return
        exp_date = exp_date or date.today().isoformat()
        entry = {
            'id': self._next_id,
            'amount': round(amount, 2),
            'category': category,
            'description': description,
            'date': exp_date,
            'added_at': datetime.now().isoformat(),
        }
        self._next_id += 1
        self.expenses.append(entry)
        self.save()
        print(f"  ✓ Added: ₹{amount:.2f} [{category}] — {description}")
        self._check_budget(category, exp_date[:7])

    def delete(self, expense_id):
        before = len(self.expenses)
        self.expenses = [e for e in self.expenses if e['id'] != expense_id]
        if len(self.expenses) < before:
            self.save()
            print(f"  ✓ Deleted expense #{expense_id}.")
        else:
            print(f"  ✗ No expense with ID {expense_id}.")

    def set_budget(self, category, amount):
        if category not in CATEGORIES:
            print(f"  ✗ Unknown category.")
            return
        self.budgets[category] = amount
        self.save()
        print(f"  ✓ Budget for '{category}' set to ₹{amount:.2f}")

    def _check_budget(self, category, month):
        spent = sum(e['amount'] for e in self.expenses
                    if e['category'] == category and e['date'].startswith(month))
        budget = self.budgets.get(category, 0)
        if budget > 0:
            pct = spent / budget * 100
            if pct >= 100:
                print(f"  🚨 BUDGET EXCEEDED for {category}: ₹{spent:.2f} / ₹{budget:.2f} ({pct:.0f}%)")
            elif pct >= 80:
                print(f"  ⚠  Budget warning for {category}: ₹{spent:.2f} / ₹{budget:.2f} ({pct:.0f}%)")

    def monthly_summary(self, year=None, month=None):
        today = date.today()
        year = year or today.year
        month = month or today.month
        prefix = f"{year}-{month:02d}"

        monthly = [e for e in self.expenses if e['date'].startswith(prefix)]
        if not monthly:
            print(f"  No expenses for {prefix}.")
            return

        by_cat = defaultdict(float)
        for e in monthly:
            by_cat[e['category']] += e['amount']

        total = sum(by_cat.values())
        month_name = datetime(year, month, 1).strftime('%B %Y')

        print(f"\n  {'═'*60}")
        print(f"  Monthly Summary — {month_name}")
        print(f"  {'─'*60}")
        print(f"  {'Category':<18} {'Spent':>10}  {'Budget':>10}  {'Status'}")
        print(f"  {'─'*60}")
        for cat in CATEGORIES:
            spent = by_cat.get(cat, 0)
            budget = self.budgets.get(cat, 0)
            if spent == 0 and budget == 0:
                continue
            pct = spent / budget * 100 if budget > 0 else 0
            bar = ('🟥' if pct >= 100 else '🟨' if pct >= 80 else '🟩') if budget > 0 else '⬜'
            print(f"  {cat:<18} ₹{spent:>9.2f}  ₹{budget:>9.2f}  {bar} {pct:.0f}%")
        print(f"  {'─'*60}")
        print(f"  {'TOTAL':<18} ₹{total:>9.2f}")
        print(f"  {'═'*60}\n")
        return monthly

    def export_monthly_report(self, year=None, month=None):
        today = date.today()
        year = year or today.year
        month = month or today.month
        prefix = f"{year}-{month:02d}"
        monthly = [e for e in self.expenses if e['date'].startswith(prefix)]

        filename = f"expense_report_{prefix}.txt"
        month_name = datetime(year, month, 1).strftime('%B %Y')
        by_cat = defaultdict(float)
        for e in monthly:
            by_cat[e['category']] += e['amount']

        with open(filename, 'w') as f:
            f.write(f"EXPENSE REPORT — {month_name}\n")
            f.write("="*60 + "\n")
            for cat in CATEGORIES:
                spent = by_cat.get(cat, 0)
                if spent > 0:
                    f.write(f"  {cat:<20} ₹{spent:.2f}\n")
            f.write("-"*60 + "\n")
            f.write(f"  TOTAL{' '*15} ₹{sum(by_cat.values()):.2f}\n\n")
            f.write("Detailed Transactions:\n")
            for e in sorted(monthly, key=lambda x: x['date']):
                f.write(f"  [{e['date']}] {e['category']:<15} ₹{e['amount']:>8.2f}  {e['description']}\n")

        print(f"  ✓ Report exported to '{filename}'")
        return filename

    def list_expenses(self, limit=20):
        shown = sorted(self.expenses, key=lambda x: x['date'], reverse=True)[:limit]
        print(f"\n  {'#':>5} {'Date':<12} {'Category':<15} {'Amount':>10}  {'Description'}")
        print(f"  {'─'*60}")
        for e in shown:
            print(f"  {e['id']:>5} {e['date']:<12} {e['category']:<15} ₹{e['amount']:>9.2f}  {e['description'][:25]}")
        print(f"  {'─'*60}")
        print(f"  Total expenses: {len(self.expenses)}\n")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Personal Expense Tracker v1.0         ║")
    print("╚══════════════════════════════════════════╝")

    tracker = ExpenseTracker()

    # Demo data
    today = date.today()
    demo = [
        (4200, "Rent",          "Monthly rent",         f"{today.year}-{today.month:02d}-01"),
        (850,  "Food",          "Groceries",            f"{today.year}-{today.month:02d}-03"),
        (320,  "Transport",     "Fuel",                 f"{today.year}-{today.month:02d}-05"),
        (1200, "Entertainment", "Movies + dining",      f"{today.year}-{today.month:02d}-07"),
        (600,  "Utilities",     "Electricity bill",     f"{today.year}-{today.month:02d}-08"),
        (450,  "Food",          "Restaurant",           f"{today.year}-{today.month:02d}-10"),
        (2200, "Shopping",      "Clothes",              f"{today.year}-{today.month:02d}-12"),
        (800,  "Healthcare",    "Doctor visit",         f"{today.year}-{today.month:02d}-14"),
        (1500, "Education",     "Online course",        f"{today.year}-{today.month:02d}-15"),
        (700,  "Food",          "Weekly groceries",     f"{today.year}-{today.month:02d}-17"),
        (5500, "Rent",          "Advance rent",         f"{today.year}-{today.month:02d}-18"),
    ]

    print("\n  Adding demo expenses:")
    for amount, cat, desc, d in demo:
        tracker.add(amount, cat, desc, d)

    tracker.list_expenses()
    tracker.monthly_summary()

    fname = tracker.export_monthly_report()

    # Interactive
    print("\n  [1] Add Expense  [2] List  [3] Monthly Summary  [4] Set Budget  [5] Quit")
    choice = input("  Choice: ").strip()
    if choice == '1':
        try:
            amt = float(input("  Amount: ₹"))
            print(f"  Categories: {', '.join(CATEGORIES)}")
            cat = input("  Category: ").strip()
            desc = input("  Description: ").strip()
            tracker.add(amt, cat, desc)
        except ValueError:
            print("  Invalid amount.")
    elif choice == '3':
        tracker.monthly_summary()
    elif choice == '4':
        cat = input("  Category: ").strip()
        try:
            amt = float(input(f"  Budget for {cat}: ₹"))
            tracker.set_budget(cat, amt)
        except ValueError:
            print("  Invalid amount.")

    # Cleanup
    for f in [DATA_FILE, fname]:
        if f and os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    main()
