"""
Shopping Cart System with Multi-Type Discount and Tax Engine
Supports add/remove/update, percentage/flat/coupon discounts, tax, itemized bill.
"""

from datetime import datetime

TAX_RATES = {
    'default': 0.18,   # GST 18%
    'food':    0.05,   # GST 5% for food
    'luxury':  0.28,   # GST 28% for luxury
}

COUPONS = {
    'SAVE10':   {'type': 'percent', 'value': 10,   'min_order': 200},
    'FLAT50':   {'type': 'flat',    'value': 50,   'min_order': 500},
    'WELCOME':  {'type': 'percent', 'value': 15,   'min_order': 0},
    'VIP25':    {'type': 'percent', 'value': 25,   'min_order': 1000},
}

CATALOG = {
    'P001': {'name': 'Laptop',        'price': 45000, 'tax_cat': 'luxury'},
    'P002': {'name': 'Headphones',    'price': 2500,  'tax_cat': 'default'},
    'P003': {'name': 'Python Book',   'price': 799,   'tax_cat': 'default'},
    'P004': {'name': 'Coffee',        'price': 350,   'tax_cat': 'food'},
    'P005': {'name': 'USB Cable',     'price': 199,   'tax_cat': 'default'},
    'P006': {'name': 'Gaming Mouse',  'price': 3200,  'tax_cat': 'luxury'},
    'P007': {'name': 'Notebook',      'price': 120,   'tax_cat': 'food'},
    'P008': {'name': 'Phone Stand',   'price': 499,   'tax_cat': 'default'},
}


class ShoppingCart:
    def __init__(self, customer_name="Guest"):
        self.customer_name = customer_name
        self.items = {}          # {product_id: {info, qty}}
        self.coupon = None
        self.flat_discount = 0
        self.created_at = datetime.now()

    def add(self, product_id, qty=1):
        product_id = product_id.upper()
        if product_id not in CATALOG:
            print(f"  ✗ Product '{product_id}' not found in catalog.")
            return
        if qty <= 0:
            print("  ✗ Quantity must be positive.")
            return
        if product_id in self.items:
            self.items[product_id]['qty'] += qty
        else:
            self.items[product_id] = {**CATALOG[product_id], 'qty': qty}
        name = CATALOG[product_id]['name']
        print(f"  ✓ Added {qty}× {name} to cart.")

    def remove(self, product_id):
        product_id = product_id.upper()
        if product_id in self.items:
            name = self.items[product_id]['name']
            del self.items[product_id]
            print(f"  ✓ Removed '{name}' from cart.")
        else:
            print(f"  ✗ '{product_id}' not in cart.")

    def update_qty(self, product_id, qty):
        product_id = product_id.upper()
        if product_id not in self.items:
            print(f"  ✗ '{product_id}' not in cart.")
            return
        if qty <= 0:
            self.remove(product_id)
        else:
            self.items[product_id]['qty'] = qty
            print(f"  ✓ Updated quantity of {self.items[product_id]['name']} to {qty}.")

    def apply_coupon(self, code):
        code = code.upper()
        if code not in COUPONS:
            print(f"  ✗ Coupon '{code}' is invalid.")
            return
        subtotal = self.subtotal_before_discount()
        coupon = COUPONS[code]
        if subtotal < coupon['min_order']:
            print(f"  ✗ Minimum order ₹{coupon['min_order']} required for '{code}'.")
            return
        self.coupon = code
        print(f"  ✓ Coupon '{code}' applied.")

    def apply_flat_discount(self, amount):
        self.flat_discount = max(0, amount)
        print(f"  ✓ Flat discount of ₹{amount:.2f} applied.")

    def subtotal_before_discount(self):
        return sum(i['price'] * i['qty'] for i in self.items.values())

    def coupon_discount_amount(self, subtotal):
        if not self.coupon:
            return 0
        coupon = COUPONS[self.coupon]
        if coupon['type'] == 'percent':
            return subtotal * coupon['value'] / 100
        elif coupon['type'] == 'flat':
            return min(coupon['value'], subtotal)
        return 0

    def compute_tax(self):
        tax_total = 0
        for item in self.items.values():
            rate = TAX_RATES.get(item.get('tax_cat', 'default'), TAX_RATES['default'])
            item_pre_tax = item['price'] * item['qty']
            tax_total += item_pre_tax * rate
        return round(tax_total, 2)

    def bill(self):
        if not self.items:
            print("  Cart is empty.")
            return

        subtotal = self.subtotal_before_discount()
        coupon_disc = round(self.coupon_discount_amount(subtotal), 2)
        after_coupon = subtotal - coupon_disc - self.flat_discount
        tax = self.compute_tax()
        grand_total = max(0, after_coupon + tax)

        print(f"\n  {'═'*62}")
        print(f"  {'ITEMIZED BILL':^60}")
        print(f"  Customer : {self.customer_name}")
        print(f"  Date     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  {'═'*62}")
        print(f"  {'#':<4} {'Item':<22} {'Price':>8}  {'Qty':>4}  {'Tax%':>5}  {'Total':>9}")
        print(f"  {'─'*62}")
        for i, (pid, item) in enumerate(self.items.items(), 1):
            rate = TAX_RATES.get(item['tax_cat'], TAX_RATES['default'])
            total = item['price'] * item['qty']
            print(f"  {i:<4} {item['name']:<22} {item['price']:>8.2f}  {item['qty']:>4}  {rate*100:>4.0f}%  {total:>9.2f}")
        print(f"  {'─'*62}")
        print(f"  {'Subtotal':<50} ₹{subtotal:>9.2f}")
        if coupon_disc:
            print(f"  {'Coupon Discount (' + self.coupon + ')':<50} -₹{coupon_disc:>8.2f}")
        if self.flat_discount:
            print(f"  {'Flat Discount':<50} -₹{self.flat_discount:>8.2f}")
        print(f"  {'GST / Tax':<50} +₹{tax:>8.2f}")
        print(f"  {'─'*62}")
        print(f"  {'GRAND TOTAL':<50} ₹{grand_total:>9.2f}")
        print(f"  {'═'*62}\n")
        return grand_total

    def view_cart(self):
        if not self.items:
            print("  Cart is empty.")
            return
        print(f"\n  Cart for: {self.customer_name}  ({len(self.items)} item types)")
        for pid, item in self.items.items():
            print(f"  [{pid}] {item['name']} × {item['qty']}  = ₹{item['price']*item['qty']:.2f}")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Shopping Cart System v1.0              ║")
    print("╚══════════════════════════════════════════╝")

    print("\n  Available Products:")
    for pid, info in CATALOG.items():
        rate = TAX_RATES.get(info['tax_cat'], TAX_RATES['default'])
        print(f"  [{pid}] {info['name']:<20} ₹{info['price']:<8}  Tax: {rate*100:.0f}%")

    cart = ShoppingCart("Rahul Gupta")
    cart.add('P001', 1)
    cart.add('P003', 2)
    cart.add('P004', 3)
    cart.add('P005', 1)
    cart.add('P006', 1)
    cart.add('P999')       # Invalid
    cart.update_qty('P004', 5)
    cart.apply_flat_discount(100)
    cart.apply_coupon('SAVE10')
    cart.apply_coupon('INVALID')
    cart.view_cart()
    cart.bill()

    # Another cart
    cart2 = ShoppingCart("Priya Mehta")
    cart2.add('P007', 10)
    cart2.add('P008', 2)
    cart2.apply_coupon('WELCOME')
    cart2.bill()


if __name__ == "__main__":
    main()
