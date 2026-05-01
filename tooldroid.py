import os
import json
import time
import sys
import subprocess

class ToolDroid:
    def __init__(self, design_capacity_mah=6000):
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
                stderr=subprocess.DEVNULL,
                shell=False
            )
            return result.decode('utf-8')
        except Exception as e:
            return None

    def fetch_core_data(self):
        try:
            raw = os.popen("termux-battery-status").read().strip()
            return json.loads(raw) if raw else None
        except:
            return None

    def fetch_advanced_data(self):
        raw_dump = self._exec_shizuku("dumpsys battery")
        if not raw_dump:
            return None
        
        adv = {}
        for line in raw_dump.split('\n'):
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    adv[parts[0].strip()] = parts[1].strip()
        return adv

    def render_ui(self):
        core = self.fetch_core_data()
        adv = self.fetch_advanced_data()
        
        if not core:
            return f"{self.colors['fail']}System Error: API Unreachable{self.colors['end']}"

        screen = [
            f"{self.colors['header']}{self.colors['bold']}--- Trizon's ToolDroid v1.1 ---{self.colors['end']}",
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
                full_cap = int(adv.get('Full charge capacity', 0)) // 1000
                curr_cap = int(adv.get('Charge counter', 0)) // 1000
                health_pct = (full_cap / self.design_capacity) * 100 if full_cap > 0 else 0
                voltage = float(adv.get('voltage', 0)) / 1000
                
                screen += [
                    f"{self.colors['shizuku']}[ SHIZUKU ENGINE ACTIVE ]{self.colors['end']}",
                    f"True Health:  {health_pct:.2f}%",
                    f"Capacity:     {curr_cap} / {full_cap} mAh",
                    f"Voltage:      {voltage:.2f}V",
                    f"Cycles:       {adv.get('Cycle count', 'N/A')}",
                    "─" * 35
                ]
            except:
                screen += [f"{self.colors['fail']}Shizuku: Data Parsing Error{self.colors['end']}", "─" * 35]
        else:
            screen += [
                f"{self.colors['warn']}Shizuku: Not Found at Path{self.colors['end']}",
                f"Looking in: {self.colors['bold']}~/storage/rish/rish{self.colors['end']}",
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
