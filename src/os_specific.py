# Everything specific to an OS is placed here
import ctypes


def detect_resolution_windows():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize


def set_wallpaper_windows(image_path):
    SPI_SETDESKWALLPAPER = 20
    return ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 2)