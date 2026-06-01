"""
JSON Data Parser with Criteria-Based Filtering and Report Generator
Loads JSON records, filters/sorts by criteria, generates summary, exports filtered results.
"""

import json
import os
from datetime import datetime
from statistics import mean, median, stdev
from collections import Counter

SAMPLE_DATA = [
    {"id": 1, "name": "Alice Sharma",    "department": "Engineering", "salary": 85000, "age": 29, "experience": 5, "rating": 4.5},
    {"id": 2, "name": "Bob Verma",       "department": "Marketing",   "salary": 62000, "age": 34, "experience": 8, "rating": 3.8},
    {"id": 3, "name": "Carol Singh",     "department": "Engineering", "salary": 92000, "age": 31, "experience": 7, "rating": 4.8},
    {"id": 4, "name": "David Kumar",     "department": "HR",          "salary": 58000, "age": 27, "experience": 3, "rating": 4.2},
    {"id": 5, "name": "Eve Patel",       "department": "Engineering", "salary": 110000,"age": 38, "experience": 12,"rating": 4.9},
    {"id": 6, "name": "Frank Nair",      "department": "Marketing",   "salary": 70000, "age": 42, "experience": 15,"rating": 3.5},
    {"id": 7, "name": "Grace Mehta",     "department": "Finance",     "salary": 88000, "age": 33, "experience": 9, "rating": 4.7},
    {"id": 8, "name": "Henry Joshi",     "department": "Engineering", "salary": 75000, "age": 26, "experience": 2, "rating": 4.1},
    {"id": 9, "name": "Irene Das",       "department": "Finance",     "salary": 95000, "age": 36, "experience": 11,"rating": 4.6},
    {"id":10, "name": "Jack Iyer",       "department": "HR",          "salary": 55000, "age": 24, "experience": 1, "rating": 3.9},
    {"id":11, "name": "Karen Roy",       "department": "Marketing",   "salary": 67000, "age": 30, "experience": 6, "rating": 4.0},
    {"id":12, "name": "Liam Bose",       "department": "Engineering", "salary": 98000, "age": 35, "experience": 10,"rating": 4.7},
    {"id":13, "name": "Maya Gupta",      "department": "Finance",     "salary": 82000, "age": 28, "experience": 4, "rating": 4.3},
    {"id":14, "name": "Nikhil Kapoor",   "department": "HR",          "salary": 60000, "age": 32, "experience": 7, "rating": 4.1},
    {"id":15, "name": "Olivia Tiwari",   "department": "Engineering", "salary": 105000,"age": 40, "experience": 14,"rating": 4.8},
]

DATA_FILE = "employees.json"
EXPORT_FILE = "filtered_results.json"


def load_data(filepath=None):
    if filepath and os.path.exists(filepath):
        with open(filepath) as f:
            return json.load(f)
    return SAMPLE_DATA


def save_data(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ Saved {len(data)} record(s) to '{filepath}'")


def filter_records(data, criteria):
    """
    criteria: dict of {field: (operator, value)}
    Operators: '=', '!=', '>', '<', '>=', '<=', 'in', 'contains'
    """
    result = []
    ops = {
        '=':  lambda a, b: a == b,
        '!=': lambda a, b: a != b,
        '>':  lambda a, b: a > b,
        '<':  lambda a, b: a < b,
        '>=': lambda a, b: a >= b,
        '<=': lambda a, b: a <= b,
        'in': lambda a, b: a in b,
        'contains': lambda a, b: b.lower() in str(a).lower(),
    }
    for record in data:
        match = True
        for field, (op, value) in criteria.items():
            rec_val = record.get(field)
            if rec_val is None:
                match = False; break
            fn = ops.get(op)
            if fn is None or not fn(rec_val, value):
                match = False; break
        if match:
            result.append(record)
    return result


def sort_records(data, sort_by, ascending=True):
    return sorted(data, key=lambda r: r.get(sort_by, 0), reverse=not ascending)


def print_records(records, title="Records", fields=None):
    if not fields:
        fields = ['id', 'name', 'department', 'salary', 'age', 'experience', 'rating']
    print(f"\n  {'═'*75}")
    print(f"  {title} ({len(records)} record(s))")
    print(f"  {'─'*75}")
    widths = {'id': 4, 'name': 18, 'department': 14, 'salary': 9, 'age': 5, 'experience': 12, 'rating': 7}
    header = "  " + "  ".join(f"{f.upper():<{widths.get(f,12)}}" for f in fields)
    print(header)
    print(f"  {'─'*75}")
    for r in records:
        row = "  " + "  ".join(f"{str(r.get(f,'')):<{widths.get(f,12)}}" for f in fields)
        print(row)
    print(f"  {'═'*75}")


def generate_report(data):
    if not data:
        print("  No data to report.")
        return

    print(f"\n  {'═'*60}")
    print(f"  DATA SUMMARY REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  {'─'*60}")
    print(f"  Total records : {len(data)}")

    # Numeric stats for salary, age, experience, rating
    for field in ['salary', 'age', 'experience', 'rating']:
        values = [r[field] for r in data if field in r]
        if values:
            print(f"\n  {field.capitalize()} Statistics:")
            print(f"    Count  : {len(values)}")
            print(f"    Min    : {min(values)}")
            print(f"    Max    : {max(values)}")
            print(f"    Mean   : {mean(values):.2f}")
            print(f"    Median : {median(values):.2f}")
            if len(values) > 1:
                print(f"    StdDev : {stdev(values):.2f}")

    # Department distribution
    depts = Counter(r.get('department', 'Unknown') for r in data)
    print(f"\n  Department Distribution:")
    for dept, count in sorted(depts.items()):
        bar = '▇' * count
        avg_sal = mean(r['salary'] for r in data if r.get('department') == dept)
        print(f"    {dept:<14} {count:>3}  {bar}  avg salary: ₹{avg_sal:,.0f}")

    # Top earners
    top = sort_records(data, 'salary', ascending=False)[:3]
    print(f"\n  Top 3 Earners:")
    for r in top:
        print(f"    {r['name']:<20} ₹{r['salary']:>8,}  ({r['department']})")

    print(f"  {'═'*60}\n")


def demo_filters(data):
    print("\n  ── Filter: Engineering dept, salary > 90000 ──")
    results = filter_records(data, {
        'department': ('=', 'Engineering'),
        'salary': ('>', 90000),
    })
    results = sort_records(results, 'salary', ascending=False)
    print_records(results, "Engineering High Earners")

    print("\n  ── Filter: Rating >= 4.5, experience >= 5 ──")
    results = filter_records(data, {
        'rating': ('>=', 4.5),
        'experience': ('>=', 5),
    })
    results = sort_records(results, 'rating', ascending=False)
    print_records(results, "High Performers")

    print("\n  ── Filter: Age between 25 and 32 ──")
    results = filter_records(data, {
        'age': ('>=', 25),
    })
    results = [r for r in results if r['age'] <= 32]
    print_records(results, "Ages 25-32", fields=['id', 'name', 'age', 'department', 'salary'])


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   JSON Data Parser & Report Generator   ║")
    print("╚══════════════════════════════════════════╝")

    # Save sample data
    save_data(SAMPLE_DATA, DATA_FILE)
    data = load_data(DATA_FILE)

    print_records(data, "All Employee Records")
    generate_report(data)
    demo_filters(data)

    # Export filtered results
    high_rated = filter_records(data, {'rating': ('>=', 4.5)})
    save_data(high_rated, EXPORT_FILE)

    # Cleanup
    for f in [DATA_FILE, EXPORT_FILE]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    main()
