import os
import json
import time
import sys
import subprocess

class ToolDroid:
    def __init__(self, design_capacity_mah=5200):
        self.design_capacity = design_capacity_mah
        self.rish_path = "/data/data/com.termux/files/home/storage/rish/rish"
        self.colors = {"header": "\033[95m", "shizuku": "\033[92m", "warn": "\033[93m", "fail": "\033[91m", "end": "\033[0m", "bold": "\033[1m"}

    def _exec_shizuku(self, command):
        try:
            return subprocess.check_output(['sh', self.rish_path, '-c', command], stderr=subprocess.DEVNULL).decode('utf-8')
        except: return None

    def fetch_core_data(self):
        try:
            raw = os.popen("termux-battery-status").read().strip()
            return json.loads(raw) if raw else None
        except: return None

    def fetch_advanced_data(self):
        raw_dump = self._exec_shizuku("dumpsys battery")
        if not raw_dump: return None
        adv = {}
        for line in raw_dump.split('\n'):
            if ":" in line:
                k, v = line.split(":", 1)
                adv[k.strip().lower()] = v.strip()
        return adv

    def render_ui(self):
        core = self.fetch_core_data()
        adv = self.fetch_advanced_data()
        if not core: return f"{self.colors['fail']}API Unreachable{self.colors['end']}"

        # Logic to find the REAL hardware capacity vs current tank level
        # We look for 'full charge capacity' or 'charge full' specifically
        f_cap_raw = adv.get('full charge capacity') or adv.get('charge full') or adv.get('charge_full')
        c_cap_raw = adv.get('charge counter') or adv.get('charge_now')
        cycle_raw = adv.get('cycle count') or adv.get('battery_cycle') or adv.get('cycle_count')

        try:
            f_cap = int(f_cap_raw) if f_cap_raw else 0
            c_cap = int(c_cap_raw) if c_cap_raw else 0
            # Convert uAh to mAh if needed
            if f_cap > 20000: f_cap //= 1000
            if c_cap > 20000: c_cap //= 1000
            
            # Use Core percentage if Shizuku capacity is missing
            current_pct = core.get('percentage', 0)
            health_pct = (f_cap / self.design_capacity) * 100 if f_cap > 0 else 100.0
            
            # Voltage Accuracy: Use core voltage if dumpsys is rounding
            voltage = core.get('voltage', 0) / 1000 if core.get('voltage') else float(adv.get('voltage', 0)) / 1000
        except:
            f_cap, c_cap, health_pct, voltage = 0, 0, 0, 0.0

        screen = [
            f"{self.colors['header']}{self.colors['bold']}--- Trizon's ToolDroid v1.3 ---{self.colors['end']}",
            f"Power State:  {core.get('status')} ({current_pct}%)",
            "─" * 35,
            f"{self.colors['shizuku']}[ SHIZUKU ENGINE ]{self.colors['end']}",
            f"True Health:  {health_pct:.1f}%",
            f"Max Cap:      {f_cap if f_cap > 0 else self.design_capacity} mAh",
            f"Current:      {c_cap} mAh",
            f"Voltage:      {voltage:.3f}V",
            f"Cycles:       {cycle_raw or 'N/A'}",
            "─" * 35,
            "LIVE REFRESH: 2S | Ctrl+C to Exit"
        ]
        return "\n".join(screen)

if __name__ == "__main__":
    try:
        while True:
            sys.stdout.write("\033[2J\033[H")
            print(ToolDroid().render_ui())
            time.sleep(2)
    except KeyboardInterrupt: pass
