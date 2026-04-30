import os
import json
import time
import sys
import subprocess

class ToolDroid:
    def __init__(self, design_capacity_mah=7000):
        self.design_capacity = design_capacity_mah
        self.colors = {
            "header": "\033[95m",
            "default": "\033[94m",
            "shizuku": "\033[92m",
            "warn": "\033[93m",
            "fail": "\033[91m",
            "end": "\033[0m",
            "bold": "\033[1m"
        }

    def _exec_shizuku(self, command):
        """Internal helper for Shizuku execution."""
        try:
            return subprocess.check_output(['rish', '-c', command], stderr=subprocess.DEVNULL).decode('utf-8')
        except:
            return None

    def fetch_core_data(self):
        """Fetches standard Android battery data via Termux API."""
        try:
            raw = os.popen("termux-battery-status").read().strip()
            return json.loads(raw) if raw else None
        except:
            return None

    def fetch_advanced_data(self):
        """Extracts hardware-level registers via Shizuku dumpsys."""
        raw_dump = self._exec_shizuku("dumpsys battery")
        if not raw_dump:
            return None
        
        adv = {}
        for line in raw_dump.split('\n'):
            if ":" in line:
                key, val = line.split(":", 1)
                adv[key.strip()] = val.strip()
        return adv

    def render_ui(self):
        core = self.fetch_core_data()
        adv = self.fetch_advanced_data()
        
        if not core:
            return f"{self.colors['fail']}System Error: API Unreachable{self.colors['end']}"

        screen = [
            f"{self.colors['header']}{self.colors['bold']}--- ToolDroid v1.0 by Trizon ---{self.colors['end']}",
            f"Power State:  {core.get('status')} ({core.get('percentage')}%)",
            f"Source:       {core.get('plugged', 'INTERNAL')}",
            "─" * 35,
            f"{self.colors['default']}[ CORE MONITOR ]{self.colors['end']}",
            f"OS Health:    {core.get('health').upper()}",
            f"Thermal:      {core.get('temperature')}°C",
            f"Flow Rate:    {core.get('current', 0)} mA",
            "─" * 35
        ]

        if adv:
            full_cap = int(adv.get('Full charge capacity', 0)) // 1000
            curr_cap = int(adv.get('Charge counter', 0)) // 1000
            health_pct = (full_cap / self.design_capacity) * 100 if full_cap > 0 else 0
            
            screen += [
                f"{self.colors['shizuku']}[ SHIZUKU ENGINE ]{self.colors['end']}",
                f"True Health:  {health_pct:.2f}%",
                f"Capacity:     {curr_cap} / {full_cap} mAh",
                f"Voltage:      {float(adv.get('voltage', 0)) / 1000:.2f}V",
                "─" * 35
            ]
        else:
            screen += [
                f"{self.colors['warn']}Shizuku: Not Authorized{self.colors['end']}",
                "Limited to basic OS metrics.",
                "─" * 35
            ]

        screen.append("LIVE REFRESH: 2S | Ctrl+C to Exit")
        return "\n".join(screen)

if __name__ == "__main__":
    app = ToolDroid()
    try:
        while True:
            sys.stdout.write("\033[2J\033[H")
            print(app.render_ui())
            time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n{app.colors['fail']}ToolDroid Terminated.{app.colors['end']}")
