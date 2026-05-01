import os
import json
import time
import sys
import subprocess
import signal

class ToolDroid:
    def __init__(self, design_capacity_mah=5200):
        self.design_capacity = design_capacity_mah
        self.rish_path = "/data/data/com.termux/files/home/storage/rish/rish"
        self.colors = {
            "header": "\033[95m",
            "core": "\033[94m",
            "shizuku": "\033[92m",
            "fail": "\033[91m",
            "end": "\033[0m",
            "bold": "\033[1m"
        }
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print(f"\n{self.colors['fail']}Session Terminated.{self.colors['end']}")
        sys.exit(0)

    def _exec_shizuku(self, command):
        try:
            return subprocess.check_output(['sh', self.rish_path, '-c', command], stderr=subprocess.DEVNULL).decode('utf-8')
        except:
            return None

    def fetch_api_data(self):
        """High-precision real-time data from Termux API."""
        try:
            raw = os.popen("termux-battery-status").read().strip()
            return json.loads(raw) if raw else None
        except:
            return None

    def fetch_hw_data(self):
        """Hardware-level registers from Shizuku."""
        raw_dump = self._exec_shizuku("dumpsys battery")
        if not raw_dump: return None
        adv = {}
        for line in raw_dump.split('\n'):
            if ":" in line:
                k, v = line.split(":", 1)
                adv[k.strip().lower()] = v.strip()
        return adv

    def render(self):
        api = self.fetch_api_data()
        hw = self.fetch_hw_data()
        
        if not api:
            return f"{self.colors['fail']}ERROR: Termux:API Unreachable{self.colors['end']}"

        pct = api.get('percentage', 0)
        status = api.get('status', 'Unknown')
        temp = api.get('temperature', 0)
        current_ma = api.get('current', 0)

        screen = [
            f"{self.colors['header']}{self.colors['bold']}--- Trizon's MonitorDroid v1.1.0 ---{self.colors['end']}",
            f"Power State:  {status} ({pct}%)",
            "─" * 35,
            f"{self.colors['core']}[ DEFAULT MONITOR ]{self.colors['end']}",
            f"Temperature:  {temp}°C",
            f"Flow Rate:    {current_ma} mA",
            "─" * 35
        ]

        if hw:
            try:
                f_cap_raw = hw.get('full charge capacity') or hw.get('charge full') or hw.get('charge_full')
                f_cap = int(f_cap_raw) if f_cap_raw else 0
                
                if f_cap > 20000: f_cap //= 1000
                
                max_val = f_cap if f_cap > 0 else self.design_capacity
                health_val = (max_val / self.design_capacity) * 100
                
                screen += [
                    f"{self.colors['shizuku']}[ SHIZUKU ACTIVE ]{self.colors['end']}",
                    f"True Health:  {health_val:.1f}%",
                    f"Max Cap:      {max_val} mAh",
                    "─" * 35
                ]
            except:
                screen += [f"{self.colors['fail']}Shizuku: Parsing Error{self.colors['end']}", "─" * 35]
        else:
            screen += [
                "\033[2mShizuku not detected/authorized.\033[0m",
                "─" * 35
            ]
            screen += [
            f"{self.colors['love']}My note to someone: Mey, I love you.{self.colors['end']}",
            f"{self.colors['love']}I hate how I am.{self.colors['end']}",
            "─" * 35,
            ] 
        screen.append("Refresh: 100 ms | Ctrl+C to Exit")
        return "\n".join(screen)

if __name__ == "__main__":
    app = ToolDroid()
    while True:
        if os.getppid() == 1: 
            break
        
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.write(app.render())
        sys.stdout.flush()
        time.sleep(0.1)
        
