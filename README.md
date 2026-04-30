# ToolDroid 🛠️

**ToolDroid** is a specialized system utility suite for Android devices (ADB). It leverages Termux and Shizuku to provide hardware insights (Default) and system-level optimizations and insights (Shizuku) that standard apps cannot reach.

## 🚀 Advanced Features
* **Hybrid Monitoring:** Seamlessly switches between standard API and Shizuku `dumpsys` data.
* **Deep Health Metrics:** Calculates actual battery degradation using hardware charge counters.
* **System Trimming:** (Shizuku Required) Integrated commands to trim system caches and free up RAM.
* **Thermal Intelligence:** Monitor real-time milliamps and thermal thresholds.

> It defaults to standard if you have Shizuku it will unlock the system features and optimizations.

## 🖼️ Gallery
![Execution](https://github.com/ActuallyTrizon/DroidPulse/raw/main/execute.jpg)
![Result](https://github.com/ActuallyTrizon/DroidPulse/raw/main/result.jpg)


## 🚀 Installation & Usage
1. Install Termux from GitHub or F-Droid.
2. Install Termux Api from GitHub or F-Droid.
3. Install dependencies:
   ```bash
   pkg update && pkg install python termux-api -y
4. Download the source code.
5. Extract the zip.
6. Run ```cd ~/storage/downloads/ToolDroid-Main/```
7. Run ```ls``` (Optional)
8. Run ```python tooldroid.py```

## Shizuku 🦊
**Activate Shizuku**
**Connect Termux with Shizuku for more features**
