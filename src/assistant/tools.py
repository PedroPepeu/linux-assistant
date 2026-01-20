import subprocess
import psutil
import platform
import shutil

def get_system_status():
    """Returns the current hardware status: CPU, RAM, and Disk usage"""
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = shutil.disk_usage("/")

    status = (
        f"System: {platform.system()} {platform.release()}\n"
        f"CPU Usage: {cpu_usage}%\n"
        f"RAM: {ram.percent}% used ({ram.available // (1024**2)}MB free)\n"
        f"Disk: {disk.percent}% used"
    )
    return {"status": status}

def control_desktop(action: str):
    """
    Controls the Linux desktop (Hyprland).
    Actions: 'next_workspace', 'toggle_mute', 'terminal'
    """
    if action == "next_workspace":
        subprocess.run(["hyprctl", "dispatch", "workspace", "+1"])
    elif action == "terminal":
        subprocess.run(["foot"]) # or your preferred terminal maybe allacrity
    return {"status": "command executed"}

AVAILABLE_TOOLS = [control_desktop, get_system_status]
