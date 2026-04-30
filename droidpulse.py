import os
import json
import time
import sys
import subprocess

def run_shizuku_cmd(cmd):
    try:
        result = subprocess.check_output(['rish', '-c', cmd], stderr=subprocess.DEVNULL)
        return result.decode('utf-8')
    except:
        return None

def get_stats():
    battery_raw = os.popen("termux-battery-status").read().strip()
    if not battery_raw:
        return "\033[91mError: Termux:API not detected.\033[0m"
    
    base = json.loads(battery_raw)
    

    temp = base.get('temperature', 0)
    thermal_status = "\033[1;32mCool\033[0m"
    if temp > 40: thermal_status = "\033[1;33mWarm\033[0m"
    if temp > 45: thermal_status = "\033[1;31mHOT (Throttling)\033[0m"

    shizuku_active = False
    max_cap, curr_cap, cycles, voltage = "N/A", "N/A", "N/A", "N/A"
    adv_raw = run_shizuku_cmd("dumpsys battery")
    
    if adv_raw:
        shizuku_active = True
        for line in adv_raw.split('\n'):
            if "Charge counter" in line:
                curr_cap = int(line.split(":")[1].strip()) // 1000 
            if "Full charge capacity" in line:
                max_cap = int(line.split(":")[1].strip()) // 1000
            if "Cycle count" in line:
                cycles = line.split(":")[1].strip()
            if "voltage" in line:
                voltage = f"{float(line.split(':')[1].strip()) / 1000:.2f}V"

    out = [
        "\033[2J\033[H",
        "\033[1;34m--- DroidPulse v1.5.8 | Device ---\033[0m",
        f"Status:          {base.get('status')} ({base.get('percentage')}%)",
        f"Charging Via:    {base.get('plugged', 'Battery')}",
        "-----------------------------------",
        "\033[1;36m[DEFAULT MONITOR]\033[0m",
        f"Health (Basic):  {base.get('health').upper()}",
        f"Temperature:     {temp}°C ({thermal_status})",
        f"Current Flow:    {base.get('current', 0)} mA",
        "-----------------------------------"
    ]

    if shizuku_active:
        health_calc = f"{(max_cap / 10000) * 100:.1f}%" if max_cap != "N/A" else "N/A"
        out += [
            "\033[1;35m[SHIZUKU ADVANCED]\033[0m",
            f"Health (Exact):  {health_calc}",
            f"Capacity:        {curr_cap} / {max_cap} mAh",
            f"Cycle Count:     {cycles} cycles",
            f"Voltage:         {voltage}",
            "-----------------------------------"
        ]
    else:
        out += ["\033[2mEnable Shizuku + rish for advanced stats\033[0m", "-----------------------------------"]

    out.append("Updating every 2s... (Ctrl+C to Exit)")
    return "\n".join(out)

if __name__ == "__main__":
    try:
        while True:
            sys.stdout.write(get_stats())
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n\033[1;31mMonitor Offline.\033[0m")
