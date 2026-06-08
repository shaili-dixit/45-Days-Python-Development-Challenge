"""
CSV File Analyzer with Statistical Summary and Data Cleaning Pipeline
Reads CSV without pandas, calculates stats, detects missing/malformed values, writes cleaned CSV.
"""

import csv
import os
import re
from statistics import mean, median, stdev, variance
from collections import Counter, defaultdict

SAMPLE_CSV = """id,name,age,salary,department,joined_date,rating
1,Alice Sharma,29,85000,Engineering,2019-03-15,4.5
2,Bob Verma,34,62000,Marketing,2016-07-22,3.8
3,Carol Singh,31,,Engineering,2017-11-01,4.8
4,David Kumar,27,58000,HR,2021-06-10,
5,Eve Patel,38,110000,Engineering,2012-01-05,4.9
6,Frank Nair,,70000,Marketing,2009-08-30,3.5
7,Grace Mehta,33,88000,Finance,2015-04-18,4.7
8,Henry Joshi,26,75000,,2022-01-11,4.1
9,,36,95000,Finance,2013-09-25,4.6
10,Jack Iyer,24,55000,HR,invalid_date,3.9
11,Karen Roy,30,67000,Marketing,2018-12-01,4.0
12,Liam Bose,35,ABC,Engineering,2014-05-20,4.7
13,Maya Gupta,28,82000,Finance,2020-08-15,4.3
14,Nikhil Kapoor,32,60000,HR,2017-03-07,4.1
15,Olivia Tiwari,40,105000,Engineering,2010-09-12,4.8
"""

SAMPLE_FILE = "employees_raw.csv"
CLEAN_FILE = "employees_clean.csv"


def write_sample_csv():
    with open(SAMPLE_FILE, 'w', newline='') as f:
        f.write(SAMPLE_CSV)
    print(f"  Sample CSV written to '{SAMPLE_FILE}'")


def read_csv(filepath):
    rows = []
    headers = []
    with open(filepath, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = list(reader.fieldnames or [])
        for row in reader:
            rows.append(dict(row))
    return headers, rows


def detect_types(rows, headers):
    """Attempt to detect column types based on data."""
    types = {}
    for col in headers:
        values = [r[col] for r in rows if r[col].strip()]
        numeric_count = 0
        date_count = 0
        for v in values:
            try:
                float(v)
                numeric_count += 1
                continue
            except ValueError:
                pass
            if re.match(r'^\d{4}-\d{2}-\d{2}$', v.strip()):
                date_count += 1
        total = len(values)
        if total == 0:
            types[col] = 'empty'
        elif numeric_count / total >= 0.7:
            types[col] = 'numeric'
        elif date_count / total >= 0.7:
            types[col] = 'date'
        else:
            types[col] = 'text'
    return types


def analyze_column(rows, col, col_type):
    values = [r[col].strip() for r in rows]
    total = len(values)
    empty = sum(1 for v in values if v == '')
    filled = [v for v in values if v != '']

    result = {
        'column': col, 'type': col_type, 'total': total,
        'missing': empty, 'filled': len(filled),
        'missing_pct': round(empty / total * 100, 1) if total else 0,
        'malformed': 0,
        'unique': len(set(filled)),
    }

    if col_type == 'numeric':
        nums = []
        malformed = 0
        for v in filled:
            try:
                nums.append(float(v))
            except ValueError:
                malformed += 1
        result['malformed'] = malformed
        if nums:
            result.update({
                'min': min(nums), 'max': max(nums),
                'mean': round(mean(nums), 2),
                'median': round(median(nums), 2),
                'stdev': round(stdev(nums), 2) if len(nums) > 1 else 0,
            })
    elif col_type == 'date':
        for v in filled:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
                result['malformed'] += 1
    elif col_type == 'text':
        result['top_values'] = Counter(filled).most_common(5)

    return result


def print_analysis_report(headers, rows, types):
    print(f"\n  {'═'*65}")
    print(f"  CSV ANALYSIS REPORT")
    print(f"  Total Rows: {len(rows)}  |  Columns: {len(headers)}")
    print(f"  {'═'*65}")

    for col in headers:
        col_type = types.get(col, 'text')
        analysis = analyze_column(rows, col, col_type)

        print(f"\n  Column: '{col}' [{col_type}]")
        print(f"    Missing  : {analysis['missing']}/{analysis['total']} ({analysis['missing_pct']}%)")
        print(f"    Malformed: {analysis['malformed']}")
        print(f"    Unique   : {analysis['unique']}")

        if col_type == 'numeric' and 'mean' in analysis:
            print(f"    Range    : {analysis['min']} – {analysis['max']}")
            print(f"    Mean     : {analysis['mean']}")
            print(f"    Median   : {analysis['median']}")
            print(f"    Std Dev  : {analysis['stdev']}")
        elif col_type == 'text' and 'top_values' in analysis:
            print(f"    Top Values: {analysis['top_values']}")

    print(f"\n  {'═'*65}")


def clean_data(rows, types):
    """Remove rows with missing required fields or malformed values."""
    required = ['id', 'name', 'salary']  # Must have these
    cleaned = []
    removed = []

    for row in rows:
        issues = []
        skip = False

        for col in required:
            if col in row and row[col].strip() == '':
                issues.append(f"missing '{col}'")
                skip = True

        # Validate numeric columns
        for col, ctype in types.items():
            if ctype == 'numeric' and row.get(col, '').strip():
                try:
                    float(row[col])
                except ValueError:
                    issues.append(f"invalid numeric '{col}'={row[col]}")
                    skip = True

        # Validate date columns
        for col, ctype in types.items():
            if ctype == 'date' and row.get(col, '').strip():
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', row[col].strip()):
                    issues.append(f"invalid date '{col}'={row[col]}")
                    skip = True

        if skip:
            removed.append({**row, '_issues': ', '.join(issues)})
        else:
            cleaned.append(row)

    return cleaned, removed


def write_clean_csv(rows, headers, filepath):
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  ✓ Cleaned CSV written: {len(rows)} rows → '{filepath}'")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   CSV Analyzer & Cleaner v1.0           ║")
    print("╚══════════════════════════════════════════╝")

    write_sample_csv()
    headers, rows = read_csv(SAMPLE_FILE)
    print(f"\n  Loaded {len(rows)} rows, {len(headers)} columns.")
    print(f"  Columns: {headers}")

    types = detect_types(rows, headers)
    print(f"\n  Detected Types: { {k: v for k, v in types.items()} }")

    print_analysis_report(headers, rows, types)

    print("\n  Running data cleaning pipeline...")
    cleaned, removed = clean_data(rows, types)

    print(f"\n  {'─'*45}")
    print(f"  Original rows : {len(rows)}")
    print(f"  Cleaned rows  : {len(cleaned)}")
    print(f"  Removed rows  : {len(removed)}")

    if removed:
        print(f"\n  Removed rows (with issues):")
        for r in removed:
            print(f"    ID={r.get('id','?')} Name={r.get('name','?')} — {r['_issues']}")

    clean_headers = [h for h in headers]
    write_clean_csv(cleaned, clean_headers, CLEAN_FILE)

    # Re-analyze cleaned data
    print("\n  Re-analyzing cleaned data...")
    h2, cleaned_rows = read_csv(CLEAN_FILE)
    types2 = detect_types(cleaned_rows, h2)
    print_analysis_report(h2, cleaned_rows, types2)

    for f in [SAMPLE_FILE, CLEAN_FILE]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    main()
