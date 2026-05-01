import os
import json
import time
import sys
import subprocess

class ToolDroid:
    def __init__(self, design_capacity_mah=5200):
        self.design_capacity = design_capacity_mah
        self.rish_path = "/data/data/com.termux/files/home/storage/rish/rish"
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
        try:
            result = subprocess.check_output(
                ['sh', self.rish_path, '-c', command], 
                stderr=subprocess.DEVNULL
            )
            return result.decode('utf-8')
        except:
            return None

    def fetch_core_data(self):
        try:
            raw = os.popen("termux-battery-status").read().strip()
            return json.loads(raw) if raw else None
        except:
            return None

    def fetch_advanced_data(self):
        raw_dump = self._exec_shizuku("dumpsys battery")
        if not raw_dump: return None
        
        adv = {}
        for line in raw_dump.split('\n'):
            if ":" in line:
                key, val = line.split(":", 1)
                # Normalize keys to lowercase for easier matching
                adv[key.strip().lower()] = val.strip()
        return adv

    def render_ui(self):
        core = self.fetch_core_data()
        adv = self.fetch_advanced_data()
        
        if not core:
            return f"{self.colors['fail']}System Error: API Unreachable{self.colors['end']}"

        screen = [
            f"{self.colors['header']}{self.colors['bold']}--- Trizon's ToolDroid v1.2 ---{self.colors['end']}",
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
            try:
                # Try to find capacity values (handling both uAh and mAh kernels)
                f_cap = int(adv.get('full charge capacity', adv.get('charge counter', 0)))
                c_cap = int(adv.get('charge counter', 0))
                
                # If value is huge, it's uAh (divide by 1000). If small, it's already mAh.
                f_cap = f_cap // 1000 if f_cap > 20000 else f_cap
                c_cap = c_cap // 1000 if c_cap > 20000 else c_cap
                
                # Use design capacity for health calc
                health_pct = (f_cap / self.design_capacity) * 100 if f_cap > 0 else 0
                volt = float(adv.get('voltage', 0)) / 1000
                
                screen += [
                    f"{self.colors['shizuku']}[ SHIZUKU ENGINE ACTIVE ]{self.colors['end']}",
                    f"True Health:  {health_pct:.1f}%",
                    f"Capacity:     {c_cap} / {f_cap} mAh",
                    f"Voltage:      {volt:.2f}V",
                    f"Cycle Count:  {adv.get('cycle count', 'N/A')}",
                    "─" * 35
                ]
            except:
                screen += [f"{self.colors['fail']}Shizuku: Data Parsing Error{self.colors['end']}", "─" * 35]
        else:
            screen += [f"{self.colors['warn']}Shizuku: Not Authorized{self.colors['end']}", "─" * 35]

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
