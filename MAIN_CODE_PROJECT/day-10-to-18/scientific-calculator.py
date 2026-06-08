"""
Scientific Multi-Operation Calculator with Memory and Session History
Supports arithmetic, power, sqrt, log, trig (deg/radian), memory, session log.
"""

import math
import os
from datetime import datetime

HISTORY_FILE = "calc_history.txt"


class ScientificCalculator:
    def __init__(self):
        self.memory = 0.0
        self.history = []
        self.angle_mode = 'deg'  # 'deg' or 'rad'
        self.last_result = 0.0

    def _to_rad(self, angle):
        return math.radians(angle) if self.angle_mode == 'deg' else angle

    def _log_entry(self, expression, result):
        entry = {
            'expr': expression,
            'result': result,
            'time': datetime.now().strftime('%H:%M:%S'),
            'mode': self.angle_mode,
        }
        self.history.append(entry)
        self.last_result = result

    # ── Basic Arithmetic ──────────────────────────────────────────
    def add(self, a, b):
        r = a + b; self._log_entry(f"{a} + {b}", r); return r

    def subtract(self, a, b):
        r = a - b; self._log_entry(f"{a} - {b}", r); return r

    def multiply(self, a, b):
        r = a * b; self._log_entry(f"{a} × {b}", r); return r

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        r = a / b; self._log_entry(f"{a} ÷ {b}", r); return r

    def modulo(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Modulo by zero undefined")
        r = a % b; self._log_entry(f"{a} mod {b}", r); return r

    # ── Power & Roots ─────────────────────────────────────────────
    def power(self, base, exp):
        r = base ** exp; self._log_entry(f"{base}^{exp}", r); return r

    def sqrt(self, n):
        if n < 0:
            raise ValueError("Cannot take sqrt of negative number")
        r = math.sqrt(n); self._log_entry(f"√{n}", r); return r

    def cbrt(self, n):
        r = math.copysign(abs(n) ** (1/3), n)
        self._log_entry(f"∛{n}", r); return r

    def nth_root(self, n, root):
        r = n ** (1 / root); self._log_entry(f"{root}√{n}", r); return r

    # ── Logarithms ────────────────────────────────────────────────
    def log10(self, n):
        if n <= 0:
            raise ValueError("Log undefined for non-positive values")
        r = math.log10(n); self._log_entry(f"log₁₀({n})", r); return r

    def ln(self, n):
        if n <= 0:
            raise ValueError("ln undefined for non-positive values")
        r = math.log(n); self._log_entry(f"ln({n})", r); return r

    def log_base(self, n, base):
        if n <= 0 or base <= 0 or base == 1:
            raise ValueError("Invalid argument for log")
        r = math.log(n, base); self._log_entry(f"log_{base}({n})", r); return r

    # ── Trigonometry ──────────────────────────────────────────────
    def sin(self, angle):
        r = math.sin(self._to_rad(angle))
        self._log_entry(f"sin({angle}°)" if self.angle_mode == 'deg' else f"sin({angle} rad)", r)
        return r

    def cos(self, angle):
        r = math.cos(self._to_rad(angle))
        self._log_entry(f"cos({angle}°)" if self.angle_mode == 'deg' else f"cos({angle} rad)", r)
        return r

    def tan(self, angle):
        rad = self._to_rad(angle)
        if abs(math.cos(rad)) < 1e-10:
            raise ValueError("tan is undefined at this angle")
        r = math.tan(rad)
        self._log_entry(f"tan({angle})", r)
        return r

    def asin(self, v):
        if not -1 <= v <= 1:
            raise ValueError("asin domain: [-1, 1]")
        r = math.degrees(math.asin(v)) if self.angle_mode == 'deg' else math.asin(v)
        self._log_entry(f"asin({v})", r); return r

    def acos(self, v):
        if not -1 <= v <= 1:
            raise ValueError("acos domain: [-1, 1]")
        r = math.degrees(math.acos(v)) if self.angle_mode == 'deg' else math.acos(v)
        self._log_entry(f"acos({v})", r); return r

    def atan(self, v):
        r = math.degrees(math.atan(v)) if self.angle_mode == 'deg' else math.atan(v)
        self._log_entry(f"atan({v})", r); return r

    # ── Memory ────────────────────────────────────────────────────
    def mem_store(self, val=None):
        self.memory = val if val is not None else self.last_result
        print(f"  M → {self.memory}")

    def mem_recall(self):
        print(f"  MR = {self.memory}")
        return self.memory

    def mem_clear(self):
        self.memory = 0.0
        print("  Memory cleared.")

    def mem_add(self, val=None):
        self.memory += val if val is not None else self.last_result
        print(f"  M += {val or self.last_result}  → M = {self.memory}")

    # ── History ───────────────────────────────────────────────────
    def print_history(self, last_n=15):
        entries = self.history[-last_n:]
        print(f"\n  Session History (last {len(entries)}):")
        print(f"  {'─'*45}")
        print(f"  {'#':<4} {'Time':<10} {'Expression':<20} {'Result':>14}")
        print(f"  {'─'*45}")
        for i, e in enumerate(entries, 1):
            result_str = f"{e['result']:.8g}"
            print(f"  {i:<4} {e['time']:<10} {e['expr']:<20} {result_str:>14}")
        print(f"  {'─'*45}")

    def save_history(self):
        with open(HISTORY_FILE, 'w') as f:
            f.write(f"Calculator Session — {datetime.now()}\n")
            f.write("="*50 + "\n")
            for e in self.history:
                f.write(f"[{e['time']}] {e['expr']} = {e['result']}\n")
        print(f"  History saved to '{HISTORY_FILE}'")

    def toggle_mode(self):
        self.angle_mode = 'rad' if self.angle_mode == 'deg' else 'deg'
        print(f"  Angle mode: {self.angle_mode.upper()}")


def run_demo(calc):
    print("\n  ── Arithmetic ──")
    pairs = [(10, 3), (100, 7), (2.5, 4.0)]
    for a, b in pairs:
        print(f"  {a} + {b} = {calc.add(a, b)}")
        print(f"  {a} - {b} = {calc.subtract(a, b)}")
        print(f"  {a} × {b} = {calc.multiply(a, b)}")
        try:
            print(f"  {a} ÷ {b} = {calc.divide(a, b):.6f}")
        except ZeroDivisionError as e:
            print(f"  ✗ {e}")

    print("\n  ── Power, Roots & Logs ──")
    for val in [2, 4, 8, 16, 100]:
        print(f"  √{val} = {calc.sqrt(val):.6f}  |  log₁₀({val}) = {calc.log10(val):.6f}  |  ln({val}) = {calc.ln(val):.6f}")

    print(f"  2^10 = {calc.power(2, 10)}")
    print(f"  ∛27 = {calc.cbrt(27):.4f}")

    print("\n  ── Trigonometry (Degrees) ──")
    for angle in [0, 30, 45, 60, 90]:
        s = calc.sin(angle)
        c = calc.cos(angle)
        try:
            t = calc.tan(angle)
        except ValueError:
            t = float('inf')
        print(f"  sin({angle:>3}°) = {s:>8.4f}  cos({angle:>3}°) = {c:>8.4f}  tan({angle:>3}°) = {t:>10.4f}")

    print("\n  ── Memory ──")
    calc.mem_store(3.14159)
    calc.mem_add(2.71828)
    pi_e = calc.mem_recall()
    print(f"  π + e ≈ {pi_e:.5f}")
    calc.mem_clear()


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Scientific Calculator v1.0            ║")
    print("╚══════════════════════════════════════════╝")

    calc = ScientificCalculator()
    run_demo(calc)
    calc.print_history()
    calc.save_history()

    print(f"\n  ── Interactive Mode (type 'help' for commands) ──")
    while True:
        cmd = input("\n  > ").strip()
        if cmd in ('quit', 'q', 'exit'):
            break
        elif cmd == 'help':
            print("  add/sub/mul/div/mod <a> <b> | pow <a> <b> | sqrt/log/ln/sin/cos/tan <n>")
            print("  ms [val] | mr | mc | history | mode | quit")
        elif cmd == 'history':
            calc.print_history()
        elif cmd == 'mode':
            calc.toggle_mode()
        elif cmd == 'mr':
            calc.mem_recall()
        elif cmd == 'mc':
            calc.mem_clear()
        else:
            parts = cmd.split()
            if not parts:
                continue
            try:
                op = parts[0]
                args = [float(x) for x in parts[1:]]
                if op == 'add' and len(args) == 2:
                    print(f"  = {calc.add(*args)}")
                elif op == 'sub' and len(args) == 2:
                    print(f"  = {calc.subtract(*args)}")
                elif op == 'mul' and len(args) == 2:
                    print(f"  = {calc.multiply(*args)}")
                elif op == 'div' and len(args) == 2:
                    print(f"  = {calc.divide(*args):.8g}")
                elif op == 'pow' and len(args) == 2:
                    print(f"  = {calc.power(*args)}")
                elif op == 'sqrt' and len(args) == 1:
                    print(f"  = {calc.sqrt(args[0]):.8g}")
                elif op == 'log' and len(args) == 1:
                    print(f"  = {calc.log10(args[0]):.8g}")
                elif op == 'ln' and len(args) == 1:
                    print(f"  = {calc.ln(args[0]):.8g}")
                elif op == 'sin' and len(args) == 1:
                    print(f"  = {calc.sin(args[0]):.8g}")
                elif op == 'cos' and len(args) == 1:
                    print(f"  = {calc.cos(args[0]):.8g}")
                elif op == 'tan' and len(args) == 1:
                    print(f"  = {calc.tan(args[0]):.8g}")
                elif op == 'ms' and len(args) >= 1:
                    calc.mem_store(args[0])
                else:
                    print(f"  ✗ Unknown command or wrong arguments.")
            except (ValueError, ZeroDivisionError) as e:
                print(f"  ✗ Error: {e}")

    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)


if __name__ == "__main__":
    main()
