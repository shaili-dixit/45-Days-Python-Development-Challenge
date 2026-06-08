"""
Multi-Alarm Clock Scheduler with Persistent Alarm Storage
Set/list/edit/delete alarms with HH:MM format; continuously checks time; triggers alerts.
"""

import json
import os
import time
import threading
from datetime import datetime

ALARM_FILE = "alarms.json"


class AlarmClock:
    def __init__(self):
        self.alarms = {}
        self._id_counter = 1
        self._running = False
        self._thread = None
        self.load()

    def load(self):
        if os.path.exists(ALARM_FILE):
            try:
                with open(ALARM_FILE) as f:
                    data = json.load(f)
                    self.alarms = {int(k): v for k, v in data.get('alarms', {}).items()}
                    self._id_counter = data.get('counter', 1)
            except:
                pass

    def save(self):
        with open(ALARM_FILE, 'w') as f:
            json.dump({'alarms': {str(k): v for k, v in self.alarms.items()},
                       'counter': self._id_counter}, f, indent=2)

    def add_alarm(self, time_str, label="Alarm", repeat=False):
        """time_str: HH:MM (24h)"""
        if not self._validate_time(time_str):
            print(f"  ✗ Invalid time format. Use HH:MM (e.g. 07:30)")
            return None
        alarm_id = self._id_counter
        self._id_counter += 1
        self.alarms[alarm_id] = {
            'id': alarm_id,
            'time': time_str,
            'label': label,
            'repeat': repeat,
            'active': True,
            'triggered_today': False,
        }
        self.save()
        print(f"  ✓ Alarm #{alarm_id} set for {time_str} — '{label}'"
              f"{' (daily)' if repeat else ''}")
        return alarm_id

    def delete_alarm(self, alarm_id):
        if alarm_id in self.alarms:
            label = self.alarms[alarm_id]['label']
            del self.alarms[alarm_id]
            self.save()
            print(f"  ✓ Deleted alarm #{alarm_id} ('{label}')")
        else:
            print(f"  ✗ No alarm with ID {alarm_id}.")

    def toggle_alarm(self, alarm_id):
        if alarm_id in self.alarms:
            self.alarms[alarm_id]['active'] = not self.alarms[alarm_id]['active']
            state = "enabled" if self.alarms[alarm_id]['active'] else "disabled"
            self.save()
            print(f"  ✓ Alarm #{alarm_id} {state}.")
        else:
            print(f"  ✗ No alarm with ID {alarm_id}.")

    def edit_alarm(self, alarm_id, new_time=None, new_label=None):
        if alarm_id not in self.alarms:
            print(f"  ✗ No alarm with ID {alarm_id}.")
            return
        alarm = self.alarms[alarm_id]
        if new_time:
            if not self._validate_time(new_time):
                print("  ✗ Invalid time format.")
                return
            alarm['time'] = new_time
        if new_label:
            alarm['label'] = new_label
        alarm['triggered_today'] = False
        self.save()
        print(f"  ✓ Alarm #{alarm_id} updated: {alarm['time']} — '{alarm['label']}'")

    def list_alarms(self):
        if not self.alarms:
            print("\n  No alarms set.")
            return
        print(f"\n  {'─'*55}")
        print(f"  {'ID':<5} {'Time':<8} {'Label':<20} {'Repeat':<8} {'Status'}")
        print(f"  {'─'*55}")
        for aid, alarm in sorted(self.alarms.items()):
            repeat = 'Daily' if alarm['repeat'] else 'Once'
            status = '✓ On' if alarm['active'] else '✗ Off'
            trig = ' [fired]' if alarm.get('triggered_today') else ''
            print(f"  {aid:<5} {alarm['time']:<8} {alarm['label'][:18]:<20} {repeat:<8} {status}{trig}")
        print(f"  {'─'*55}")

    def _validate_time(self, t):
        parts = t.strip().split(':')
        if len(parts) != 2:
            return False
        try:
            h, m = int(parts[0]), int(parts[1])
            return 0 <= h <= 23 and 0 <= m <= 59
        except ValueError:
            return False

    def _ring(self, alarm):
        """Simulate alarm going off."""
        print(f"\n  🔔🔔🔔 ALARM! [{alarm['time']}] — {alarm['label']} 🔔🔔🔔")
        for _ in range(3):
            print('\a', end='', flush=True)
            time.sleep(0.5)

    def check_alarms_once(self):
        """Check all alarms against current time."""
        now = datetime.now()
        current = now.strftime('%H:%M')
        triggered = []

        for aid, alarm in list(self.alarms.items()):
            if not alarm['active']:
                continue
            if alarm.get('triggered_today'):
                continue
            if alarm['time'] == current:
                self._ring(alarm)
                alarm['triggered_today'] = True
                triggered.append(aid)
                if not alarm['repeat']:
                    alarm['active'] = False

        if triggered:
            self.save()

        return triggered

    def _reset_daily_flags(self):
        """Reset triggered_today flags at midnight."""
        for alarm in self.alarms.values():
            alarm['triggered_today'] = False
        self.save()

    def _monitor_loop(self):
        last_day = datetime.now().day
        print("  ⏰ Alarm monitor started. Press Ctrl+C or select menu option to stop.")
        while self._running:
            now = datetime.now()
            if now.day != last_day:
                self._reset_daily_flags()
                last_day = now.day
            self.check_alarms_once()
            time.sleep(30)  # Check every 30 seconds in real use

    def start_monitoring(self, background=True):
        if self._running:
            print("  Monitor already running.")
            return
        self._running = True
        if background:
            self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._thread.start()
        else:
            self._monitor_loop()

    def stop_monitoring(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        print("  ⏸ Alarm monitor stopped.")


def simulate_alarm_trigger(clock):
    """Demo: create an alarm for right now + 1 minute."""
    now = datetime.now()
    target = now.replace(minute=(now.minute + 1) % 60,
                         hour=(now.hour + (1 if now.minute == 59 else 0)) % 24)
    t_str = target.strftime('%H:%M')
    alarm_id = clock.add_alarm(t_str, "Demo Alarm — 1 min from now")
    return alarm_id, t_str


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Multi-Alarm Clock Scheduler v1.0      ║")
    print("╚══════════════════════════════════════════╝")

    clock = AlarmClock()

    # Demo alarms
    clock.add_alarm("07:00", "Morning Wake Up", repeat=True)
    clock.add_alarm("12:30", "Lunch Break", repeat=True)
    clock.add_alarm("18:00", "Evening Walk", repeat=False)
    clock.add_alarm("22:00", "Bedtime Reminder", repeat=True)

    clock.list_alarms()

    clock.edit_alarm(2, new_time="12:45", new_label="Lunch (updated)")
    clock.toggle_alarm(3)
    clock.list_alarms()

    # Demo immediate trigger
    demo_id, t_str = simulate_alarm_trigger(clock)
    print(f"\n  Demo: Alarm #{demo_id} set for {t_str}.")
    print(f"  Current time: {datetime.now().strftime('%H:%M:%S')}")

    while True:
        print("\n  [1] Add Alarm  [2] List  [3] Edit  [4] Delete  [5] Toggle  [6] Check Now  [7] Quit")
        choice = input("  Choice: ").strip()
        if choice == '7':
            break
        elif choice == '1':
            t = input("  Time (HH:MM): ").strip()
            label = input("  Label: ").strip() or "Alarm"
            rep = input("  Repeat daily? (y/n): ").strip().lower() == 'y'
            clock.add_alarm(t, label, repeat=rep)
        elif choice == '2':
            clock.list_alarms()
        elif choice == '3':
            try:
                aid = int(input("  Alarm ID: "))
                nt = input("  New time (or Enter to skip): ").strip() or None
                nl = input("  New label (or Enter to skip): ").strip() or None
                clock.edit_alarm(aid, nt, nl)
            except ValueError:
                print("  Invalid ID.")
        elif choice == '4':
            try:
                aid = int(input("  Alarm ID to delete: "))
                clock.delete_alarm(aid)
            except ValueError:
                print("  Invalid ID.")
        elif choice == '5':
            try:
                aid = int(input("  Alarm ID to toggle: "))
                clock.toggle_alarm(aid)
            except ValueError:
                print("  Invalid ID.")
        elif choice == '6':
            triggered = clock.check_alarms_once()
            if not triggered:
                print(f"  No alarms triggered at {datetime.now().strftime('%H:%M')}.")
        else:
            print("  Invalid choice.")

    if os.path.exists(ALARM_FILE):
        os.remove(ALARM_FILE)
    print("  Goodbye!")


if __name__ == "__main__":
    main()
