"""
Library Book Management System with Borrow Tracking and Fine Calculation
Tracks books, borrow/return with due dates, overdue list, and fine calculation.
"""

import json
import os
from datetime import datetime, timedelta

FINE_PER_DAY = 2.50   # ₹ per day overdue
DATA_FILE = "library.json"

SAMPLE_BOOKS = [
    {"isbn": "978-0-13-110362-7", "title": "The C Programming Language", "author": "Kernighan & Ritchie", "genre": "Programming", "copies": 3},
    {"isbn": "978-0-20-131699-9", "title": "The Pragmatic Programmer",   "author": "Hunt & Thomas",       "genre": "Programming", "copies": 2},
    {"isbn": "978-0-59-651798-1", "title": "Learning Python",            "author": "Mark Lutz",           "genre": "Programming", "copies": 4},
    {"isbn": "978-0-06-112008-4", "title": "To Kill a Mockingbird",      "author": "Harper Lee",          "genre": "Fiction",     "copies": 2},
    {"isbn": "978-0-74-325045-5", "title": "1984",                       "author": "George Orwell",       "genre": "Dystopia",    "copies": 3},
    {"isbn": "978-0-06-093546-9", "title": "To Kill a Mockingbird",      "author": "Harper Lee",          "genre": "Fiction",     "copies": 2},
    {"isbn": "978-0-14-028329-7", "title": "Brave New World",            "author": "Aldous Huxley",       "genre": "Dystopia",    "copies": 2},
    {"isbn": "978-0-14-118776-1", "title": "The Great Gatsby",           "author": "F. Scott Fitzgerald", "genre": "Fiction",     "copies": 3},
]


class Library:
    def __init__(self):
        self.books = {}    # isbn -> book_info
        self.loans = {}    # loan_id -> loan_info
        self._loan_counter = 1
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE) as f:
                    data = json.load(f)
                    self.books = data.get('books', {})
                    self.loans = data.get('loans', {})
                    self._loan_counter = data.get('counter', 1)
                    return
            except:
                pass
        # Load samples
        for book in SAMPLE_BOOKS:
            isbn = book['isbn']
            self.books[isbn] = {**book, 'available': book['copies']}

    def save(self):
        with open(DATA_FILE, 'w') as f:
            json.dump({'books': self.books, 'loans': self.loans, 'counter': self._loan_counter}, f, indent=2)

    def add_book(self, isbn, title, author, genre, copies=1):
        if isbn in self.books:
            self.books[isbn]['copies'] += copies
            self.books[isbn]['available'] += copies
            print(f"  ✓ Added {copies} more copy/copies of '{title}'.")
        else:
            self.books[isbn] = {'isbn': isbn, 'title': title, 'author': author,
                                'genre': genre, 'copies': copies, 'available': copies}
            print(f"  ✓ New book added: '{title}'.")
        self.save()

    def search(self, query, field='all'):
        query = query.lower()
        results = []
        for b in self.books.values():
            if field == 'all':
                if (query in b['title'].lower() or query in b['author'].lower()
                        or query in b['genre'].lower() or query in b['isbn']):
                    results.append(b)
            elif query in b.get(field, '').lower():
                results.append(b)
        return results

    def borrow(self, isbn, member_name, days=14):
        if isbn not in self.books:
            print(f"  ✗ Book not found: {isbn}")
            return None
        book = self.books[isbn]
        if book['available'] <= 0:
            print(f"  ✗ '{book['title']}' is not available.")
            return None

        loan_id = f"L{self._loan_counter:06d}"
        self._loan_counter += 1
        due = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        self.loans[loan_id] = {
            'loan_id': loan_id, 'isbn': isbn, 'title': book['title'],
            'member': member_name, 'borrow_date': datetime.now().strftime('%Y-%m-%d'),
            'due_date': due, 'returned': False, 'return_date': None,
        }
        self.books[isbn]['available'] -= 1
        self.save()
        print(f"  ✓ Loaned: '{book['title']}' to {member_name}. Due: {due} [{loan_id}]")
        return loan_id

    def return_book(self, loan_id):
        if loan_id not in self.loans:
            print(f"  ✗ Loan ID '{loan_id}' not found.")
            return
        loan = self.loans[loan_id]
        if loan['returned']:
            print(f"  ✗ Already returned.")
            return
        loan['returned'] = True
        loan['return_date'] = datetime.now().strftime('%Y-%m-%d')
        self.books[loan['isbn']]['available'] += 1
        fine = self.calculate_fine(loan)
        self.save()
        print(f"  ✓ Returned: '{loan['title']}' by {loan['member']}.")
        if fine > 0:
            print(f"  ⚠  Fine due: ₹{fine:.2f}")
        else:
            print(f"  ✓ No fine.")

    def calculate_fine(self, loan):
        due = datetime.strptime(loan['due_date'], '%Y-%m-%d')
        end = datetime.now() if not loan['returned'] else datetime.strptime(loan['return_date'], '%Y-%m-%d')
        overdue_days = max(0, (end - due).days)
        return overdue_days * FINE_PER_DAY

    def overdue_books(self):
        today = datetime.now()
        overdue = []
        for loan in self.loans.values():
            if not loan['returned']:
                due = datetime.strptime(loan['due_date'], '%Y-%m-%d')
                if today > due:
                    days_late = (today - due).days
                    fine = days_late * FINE_PER_DAY
                    overdue.append({**loan, 'days_late': days_late, 'fine': fine})
        return sorted(overdue, key=lambda x: -x['days_late'])

    def print_catalog(self):
        print(f"\n  {'═'*75}")
        print(f"  {'LIBRARY CATALOG':^73}")
        print(f"  {'─'*75}")
        print(f"  {'ISBN':<22} {'Title':<35} {'Available':>9}  {'Genre'}")
        print(f"  {'─'*75}")
        for b in sorted(self.books.values(), key=lambda x: x['title']):
            avail = f"{b['available']}/{b['copies']}"
            status = "" if b['available'] > 0 else " [UNAVAILABLE]"
            print(f"  {b['isbn']:<22} {b['title'][:33]:<35} {avail:>9}  {b['genre']}{status}")
        print(f"  {'═'*75}\n")

    def print_overdue(self):
        overdue = self.overdue_books()
        print(f"\n  Overdue Books ({len(overdue)}):")
        if not overdue:
            print("  No overdue books.")
            return
        print(f"  {'─'*65}")
        for l in overdue:
            print(f"  {l['loan_id']}  '{l['title'][:30]}'  {l['member']}")
            print(f"    Due: {l['due_date']}  Days Late: {l['days_late']}  Fine: ₹{l['fine']:.2f}")
        print(f"  {'─'*65}")

    def active_loans(self):
        loans = [l for l in self.loans.values() if not l['returned']]
        print(f"\n  Active Loans ({len(loans)}):")
        print(f"  {'─'*60}")
        for l in loans:
            print(f"  {l['loan_id']}  '{l['title'][:30]}'  {l['member']:<15} Due: {l['due_date']}")
        print(f"  {'─'*60}")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Library Management System v1.0        ║")
    print("╚══════════════════════════════════════════╝")

    lib = Library()
    lib.print_catalog()

    # Demo borrowing
    l1 = lib.borrow("978-0-59-651798-1", "Alice Sharma", days=14)
    l2 = lib.borrow("978-0-74-325045-5", "Bob Verma",    days=7)
    l3 = lib.borrow("978-0-14-028329-7", "Carol Singh",  days=10)

    lib.active_loans()

    # Simulate return
    if l1:
        lib.return_book(l1)

    # Search
    print("\n  Search results for 'Python':")
    results = lib.search('python')
    for r in results:
        print(f"  → {r['title']} by {r['author']} | Available: {r['available']}/{r['copies']}")

    lib.print_overdue()

    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


if __name__ == "__main__":
    main()
