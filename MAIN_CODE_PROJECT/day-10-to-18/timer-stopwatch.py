"""
Countdown Timer and Multi-Lap Stopwatch with Live Display
Countdown with alert, stopwatch with lap tracking, live-updating time display.
"""

import time
import sys
import os
from datetime import timedelta


def clear_line():
    sys.stdout.write('\r' + ' ' * 60 + '\r')
    sys.stdout.flush()


def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 100)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:02d}"
    return f"{m:02d}:{s:02d}.{ms:02d}"


def alert_sound(times=3):
    """Terminal bell alert."""
    for _ in range(times):
        sys.stdout.write('\a')
        sys.stdout.flush()
        time.sleep(0.3)


def countdown_timer(hours=0, minutes=0, seconds=0, label=""):
    total = hours * 3600 + minutes * 60 + seconds
    if total <= 0:
        print("  ✗ Please enter a positive duration.")
        return

    target_label = label or "Timer"
    print(f"\n  ⏱  Countdown: {format_time(total)} ({target_label})")
    print("  Press Ctrl+C to cancel.\n")

    start = time.time()
    elapsed = 0

    try:
        while elapsed < total:
            remaining = total - elapsed
            bar_pct = 1 - (remaining / total)
            bar_len = 30
            filled = int(bar_pct * bar_len)
            bar = '█' * filled + '░' * (bar_len - filled)
            pct = bar_pct * 100
            display = f"  [{bar}] {pct:>5.1f}%  {format_time(remaining)} remaining"
            sys.stdout.write('\r' + display)
            sys.stdout.flush()
            time.sleep(0.05)
            elapsed = time.time() - start

        clear_line()
        print(f"\n  🔔 TIME'S UP! '{target_label}' completed!")
        alert_sound()

    except KeyboardInterrupt:
        clear_line()
        print(f"\n  ⚠  Countdown cancelled at {format_time(total - elapsed)} remaining.")


class Stopwatch:
    def __init__(self):
        self.laps = []
        self._start = None
        self._paused_at = None
        self._total_pause = 0
        self._running = False

    def start(self):
        if self._running:
            print("  Stopwatch already running.")
            return
        self._start = time.time()
        self._total_pause = 0
        self._running = True
        print("  ▶ Stopwatch started.")

    def pause(self):
        if not self._running:
            return
        self._paused_at = time.time()
        self._running = False
        print(f"  ⏸  Paused at {format_time(self.elapsed())}")

    def resume(self):
        if self._running or self._start is None:
            return
        self._total_pause += time.time() - self._paused_at
        self._running = True
        print("  ▶ Resumed.")

    def lap(self):
        if not self._running:
            print("  Stopwatch is not running.")
            return
        lap_time = self.elapsed()
        prev = self.laps[-1]['total'] if self.laps else 0
        self.laps.append({'lap': len(self.laps) + 1, 'split': lap_time - prev, 'total': lap_time})
        print(f"  🏁 Lap {len(self.laps):>3} — Split: {format_time(lap_time - prev)}  Total: {format_time(lap_time)}")

    def stop(self):
        total = self.elapsed()
        self._running = False
        self._start = None
        return total

    def reset(self):
        self.__init__()
        print("  ↺  Stopwatch reset.")

    def elapsed(self):
        if self._start is None:
            return 0
        now = time.time() if self._running else (self._paused_at or time.time())
        return now - self._start - self._total_pause

    def run_live(self):
        """Live-updating display until user presses Enter."""
        print("  Commands while running:  [L] Lap  [P] Pause/Resume  [S] Stop")
        print("  (This demo runs for 5 seconds with auto-laps)\n")

        self.start()
        try:
            import threading

            def auto_lap_and_stop():
                for i in range(5):
                    time.sleep(1)
                    self.lap()
                self.pause()

            t = threading.Thread(target=auto_lap_and_stop, daemon=True)
            t.start()

            while self._running or t.is_alive():
                e = self.elapsed()
                sys.stdout.write(f'\r  ⏱  Elapsed: {format_time(e)}  Laps: {len(self.laps)}   ')
                sys.stdout.flush()
                time.sleep(0.05)

            t.join()
            total = self.stop()
            clear_line()
            print(f"\n  ■ Stopped. Total: {format_time(total)}")

        except KeyboardInterrupt:
            total = self.stop()
            clear_line()
            print(f"\n  ■ Stopped manually. Total: {format_time(total)}")

    def print_lap_table(self):
        if not self.laps:
            print("  No laps recorded.")
            return
        fastest = min(self.laps, key=lambda l: l['split'])
        slowest = max(self.laps, key=lambda l: l['split'])

        print(f"\n  {'─'*50}")
        print(f"  {'Lap':>5}  {'Split':>12}  {'Total':>12}  {'Note'}")
        print(f"  {'─'*50}")
        for lap in self.laps:
            note = ""
            if lap['lap'] == fastest['lap']:
                note = "⚡ FASTEST"
            elif lap['lap'] == slowest['lap']:
                note = "🐢 SLOWEST"
            print(f"  {lap['lap']:>5}  {format_time(lap['split']):>12}  {format_time(lap['total']):>12}  {note}")
        avg = sum(l['split'] for l in self.laps) / len(self.laps)
        print(f"  {'─'*50}")
        print(f"  Average lap time: {format_time(avg)}")
        print(f"  {'─'*50}\n")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Countdown Timer & Stopwatch v1.0       ║")
    print("╚══════════════════════════════════════════╝")

    while True:
        print("\n  [1] Countdown Timer  [2] Stopwatch Demo  [3] Quit")
        choice = input("  Choice: ").strip()
        if choice == '1':
            try:
                h = int(input("  Hours   : ") or "0")
                m = int(input("  Minutes : ") or "0")
                s = int(input("  Seconds : ") or "0")
                label = input("  Label (optional): ").strip()
                countdown_timer(h, m, s, label)
            except ValueError:
                print("  ✗ Invalid input.")
        elif choice == '2':
            sw = Stopwatch()
            sw.run_live()
            sw.print_lap_table()
        elif choice == '3':
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
