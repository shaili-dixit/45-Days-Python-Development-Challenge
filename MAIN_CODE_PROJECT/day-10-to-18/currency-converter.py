"""
Multi-Currency Converter with Rate Table and Favourite Pairs
Supports 12+ currencies, full rate table, and favourite pairs quick-access.
"""

from datetime import datetime

# Exchange rates relative to USD (as of demo date)
BASE_CURRENCY = 'USD'
RATES = {
    'USD': 1.0,
    'EUR': 0.9198,
    'GBP': 0.7912,
    'INR': 83.47,
    'JPY': 149.85,
    'CAD': 1.3648,
    'AUD': 1.5523,
    'CHF': 0.8972,
    'CNY': 7.2441,
    'MXN': 17.12,
    'BRL': 4.9712,
    'SGD': 1.3489,
    'AED': 3.6725,
    'KRW': 1325.0,
    'SEK': 10.6134,
}

CURRENCY_INFO = {
    'USD': ('US Dollar',          '$'),
    'EUR': ('Euro',               '€'),
    'GBP': ('British Pound',      '£'),
    'INR': ('Indian Rupee',       '₹'),
    'JPY': ('Japanese Yen',       '¥'),
    'CAD': ('Canadian Dollar',    'C$'),
    'AUD': ('Australian Dollar',  'A$'),
    'CHF': ('Swiss Franc',        'Fr'),
    'CNY': ('Chinese Yuan',       '¥'),
    'MXN': ('Mexican Peso',       '$'),
    'BRL': ('Brazilian Real',     'R$'),
    'SGD': ('Singapore Dollar',   'S$'),
    'AED': ('UAE Dirham',         'د.إ'),
    'KRW': ('South Korean Won',   '₩'),
    'SEK': ('Swedish Krona',      'kr'),
}


def convert(amount, from_curr, to_curr):
    from_curr = from_curr.upper()
    to_curr = to_curr.upper()
    if from_curr not in RATES:
        raise ValueError(f"Unknown currency: {from_curr}")
    if to_curr not in RATES:
        raise ValueError(f"Unknown currency: {to_curr}")
    # Convert to USD then to target
    in_usd = amount / RATES[from_curr]
    return in_usd * RATES[to_curr]


def symbol(curr):
    return CURRENCY_INFO.get(curr.upper(), ('?', curr))[1]


def name(curr):
    return CURRENCY_INFO.get(curr.upper(), (curr, '?'))[0]


def format_amount(amount, curr):
    curr = curr.upper()
    sym = symbol(curr)
    if amount >= 1_000_000:
        return f"{sym}{amount/1_000_000:.3f}M"
    if amount >= 1_000:
        return f"{sym}{amount:,.2f}"
    return f"{sym}{amount:.4f}"


def print_conversion(amount, from_curr, to_curr):
    result = convert(amount, from_curr, to_curr)
    rate = RATES[to_curr.upper()] / RATES[from_curr.upper()]
    print(f"  {format_amount(amount, from_curr)} ({name(from_curr)})"
          f"  =  {format_amount(result, to_curr)} ({name(to_curr)})")
    print(f"     Rate: 1 {from_curr} = {rate:.6f} {to_curr}")
    return result


def print_rate_table(base_curr):
    base_curr = base_curr.upper()
    if base_curr not in RATES:
        print(f"  Unknown currency: {base_curr}")
        return
    print(f"\n  {'═'*60}")
    print(f"  Exchange Rate Table — Base: {base_curr} ({name(base_curr)})")
    print(f"  As of: {datetime.now().strftime('%Y-%m-%d %H:%M')} (demo rates)")
    print(f"  {'═'*60}")
    print(f"  {'Currency':<8} {'Name':<22} {'Symbol':<6} {'Rate':>12}")
    print(f"  {'─'*60}")
    for curr in sorted(RATES):
        if curr == base_curr:
            continue
        rate = convert(1, base_curr, curr)
        sym = symbol(curr)
        n = name(curr)
        print(f"  {curr:<8} {n:<22} {sym:<6} {rate:>12.4f}")
    print(f"  {'═'*60}\n")


class FavouritePairs:
    def __init__(self):
        self.pairs = []

    def add(self, from_curr, to_curr, label=None):
        from_curr = from_curr.upper()
        to_curr = to_curr.upper()
        if from_curr not in RATES or to_curr not in RATES:
            print(f"  ✗ Invalid currency pair: {from_curr}/{to_curr}")
            return
        pair = {'from': from_curr, 'to': to_curr, 'label': label or f"{from_curr}→{to_curr}"}
        if pair not in self.pairs:
            self.pairs.append(pair)
            print(f"  ✓ Added favourite: {pair['label']}")

    def remove(self, from_curr, to_curr):
        self.pairs = [p for p in self.pairs
                      if not (p['from'] == from_curr.upper() and p['to'] == to_curr.upper())]

    def quick_convert(self, amount):
        if not self.pairs:
            print("  No favourite pairs saved.")
            return
        print(f"\n  Quick Convert — {format_amount(amount, 'USD')} equivalent:")
        print(f"  {'─'*55}")
        for p in self.pairs:
            result = convert(amount, p['from'], p['to'])
            label = p['label']
            print(f"  {label:<15} {format_amount(amount, p['from'])} → {format_amount(result, p['to'])}")
        print(f"  {'─'*55}")

    def list_pairs(self):
        if not self.pairs:
            print("  No favourites saved.")
        for i, p in enumerate(self.pairs, 1):
            rate = convert(1, p['from'], p['to'])
            print(f"  {i}. {p['label']:<15}  Rate: 1 {p['from']} = {rate:.4f} {p['to']}")


def batch_convert_demo():
    conversions = [
        (100, 'USD', 'INR'),
        (50,  'EUR', 'GBP'),
        (1000, 'INR', 'USD'),
        (200, 'JPY', 'CNY'),
        (75, 'CAD', 'AUD'),
        (500, 'USD', 'KRW'),
    ]
    print(f"\n  {'─'*55}")
    print(f"  Batch Conversions:")
    print(f"  {'─'*55}")
    for amount, fr, to in conversions:
        print_conversion(amount, fr, to)
        print()


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Multi-Currency Converter v1.0          ║")
    print("╚══════════════════════════════════════════╝")

    # Setup favourites
    favs = FavouritePairs()
    favs.add('USD', 'INR', 'USD→INR')
    favs.add('EUR', 'GBP', 'EUR→GBP')
    favs.add('USD', 'JPY', 'USD→JPY')
    favs.add('INR', 'USD', 'INR→USD')

    batch_convert_demo()

    print_rate_table('USD')
    print_rate_table('INR')

    print("  Favourite Pairs:")
    favs.list_pairs()
    favs.quick_convert(100)

    print("\n  ── Interactive Mode ──")
    while True:
        print("\n  [1] Convert  [2] Rate Table  [3] Favourite Quick Convert  [4] Quit")
        choice = input("  Choice: ").strip()
        if choice == '4':
            break
        elif choice == '1':
            try:
                amt = float(input("  Amount: "))
                fr = input("  From currency (e.g. USD): ").strip().upper()
                to = input("  To currency   (e.g. INR): ").strip().upper()
                print_conversion(amt, fr, to)
            except (ValueError, Exception) as e:
                print(f"  ✗ {e}")
        elif choice == '2':
            base = input("  Base currency: ").strip()
            print_rate_table(base)
        elif choice == '3':
            try:
                amt = float(input("  Amount (in 'from' currency): "))
                favs.quick_convert(amt)
            except ValueError:
                print("  Invalid amount.")
        else:
            print("  Invalid choice.")

    print("  Goodbye!")


if __name__ == "__main__":
    main()
