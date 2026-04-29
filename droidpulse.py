import os
import json
import time

def get_stats():
    try:
        battery_raw = os.popen("termux-battery-status").read()
        if not battery_raw:
            return "Error: Termux-API not responsive."
        
        data = json.loads(battery_raw)
        
        output = [
            "\033[H\033[J",
            "--- DroidPulse Monitor ---",
            f"Battery Level: {data.get('percentage', 'N/A')}%",
            f"Temperature:   {data.get('temperature', 'N/A')}°C",
            f"Status:        {data.get('status', 'N/A')}",
            f"Health:        {data.get('health', 'N/A')}",
            f"Current:       {data.get('current', 'N/A')} mA",
            "--------------------------",
            "Ctrl+C to exit"
        ]
        return "\n".join(output)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    try:
        while True:
            print(get_stats())
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nMonitor stopped.")
