# ToolDroid 🛠️

**ToolDroid** is a specialized system utility suite for Android devices (ADB). It leverages Termux and Shizuku to provide hardware insights (Default) and hidden insights (Shizuku) that standard apps cannot reach.

## 🚀 Advanced Features
* **Simple Monitoring:** standard API and Shizuku `dumpsys` data.
* **Health Metrics:** Calculates actual battery health with Shizuku.
* **Thermal:** Monitor  charging current and temperature.

> It hides shizuku features if you don't have it enabled and connected.

## 🖼️ Gallery
![Result](https://github.com/ActuallyTrizon/DroidPulse/raw/main/result.jpg)


## 🚀 Installation & Usage
1. Install Termux from GitHub or F-Droid.
2. Install Termux Api from GitHub or F-Droid.
3. Install dependencies:
   ```
   pkg update && pkg install python termux-api -y
4. Download the source code.
5. Extract the zip.
6. Run ```
   cd ~/storage/downloads/ToolDroid-Main/```
8. Run ```ls``` (Optional)
9. Run ```python tooldroid.py```

## Shizuku 🦊
**Activate Shizuku**
1. export rish
2. make folder in termux's storage named ```rish```
3. move the ```rish``` to the rish folder
4. in termux run ```cd ~/storage/rish/```
5. run ```sh rish```
6. quit session by pressing quit in notifications
7. Now you can enjoy!

# You must have Shizuku running
