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
    
    shizuku_active = False
    max_cap, curr_cap, health_pct = "N/A", "N/A", "N/A"
    adv_raw = run_shizuku_cmd("dumpsys battery")
    
    if adv_raw:
        shizuku_active = True
        for line in adv_raw.split('\n'):
            if "Charge counter" in line:
                curr_cap = int(line.split(":")[1].strip()) // 1000 
            if "Full charge capacity" in line:
                max_cap = int(line.split(":")[1].strip()) // 1000
        
        if isinstance(max_cap, int) and max_cap > 0:
            health_pct = f"{(max_cap / 5200) * 100:.1f}%"

    out = [
        "\033[2J\033[H",
        "\033[1;34m--- DroidPulse v2.1 ---\033[0m",
        f"Charging State:  {base.get('status')} ({base.get('percentage')}%)",
        "-----------------------------------",
        "\033[1;36m[DEFAULT MONITOR]\033[0m",
        f"Health (OS):     {base.get('health').upper()}",
        f"Temperature:     {temp}°C",
        f"Current:         {base.get('current', 0)} mA",
        "-----------------------------------"
    ]

    if shizuku_active:
        out += [
            "\033[1;35m[SHIZUKU FEATURES]\033[0m",
            f"Health (Exact):  {health_pct}",
            f"Max Capacity:    {max_cap} mAh",
            f"Current Charge:  {curr_cap} mAh",
            "-----------------------------------"
        ]
    else:
        out += ["\033[2mShizuku features disabled\033[0m", "-----------------------------------"]

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
                curr_cap = int(line.split(":")[1].strip()) // 1000 
            if "Full charge capacity" in line:
                max_cap = int(line.split(":")[1].strip()) // 1000
            if "Cycle count" in line:
                cycles = line.split(":")[1].strip()
            if "voltage" in line:
                voltage = f"{float(line.split(':')[1].strip()) / 1000:.2f}V"

    # 3. Building the Interface
    out = [
        "\033[2J\033[H",
        "\033[1;34m--- DroidPulse v2.0 | Honor X6b ---\033[0m",
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
        # Honor X6b Design Capacity is roughly 5200mAh
        health_calc = f"{(max_cap / 5200) * 100:.1f}%" if max_cap != "N/A" else "N/A"
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
                # current mAh
                curr_cap = int(line.split(":")[1].strip()) // 1000 
            if "Full charge capacity" in line:
                # max mAh
                max_cap = int(line.split(":")[1].strip()) // 1000
        
        if isinstance(max_cap, int) and max_cap > 0:
            # Simple health calc: (Current Max / Design Capacity)
            # Note: 5000 is typical for Honor X6b, adjust if needed
            health_pct = f"{(max_cap / 5200) * 100:.1f}%" 

    # UI Output
    output = [
        "\033[2J\033[H",
        "\033[1;34m--- DroidPulse Hardware Monitor ---\033[0m",
        f"Shizuku Status:  {'✅ Authorized' if shizuku_active else '❌ Not Detected'}",
        f"Battery Level:   {base_data.get('percentage')}%",
        f"Temperature:     {base_data.get('temperature')}°C",
        f"Power Current:   {base_data.get('current', 'N/A')} mA",
        "-----------------------------------",
        f"Health (Actual): {health_pct}",
        f"Max Capacity:    {max_cap} mAh",
        f"Current Charge:  {curr_cap} mAh",
        "-----------------------------------",
        "Updating every 2s... (Ctrl+C to Stop)"
    ]
    return "\n".join(output)

if __name__ == "__main__":
    # Check for rish installation first
    if not os.path.exists("/data/data/com.termux/files/usr/bin/rish"):
        print("\033[1;33mHint: To see Max Capacity, install 'shizuku' and 'rish' in Termux.\033[0m")
    
    try:
        while True:
            sys.stdout.write(get_stats())
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n\033[1;31mMonitor Disconnected.\033[0m")
