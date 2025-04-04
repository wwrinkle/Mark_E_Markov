from core.const import DEVICE_NAME
from core.pyaudio_client import client as pyaudio_client


def get_device_index():
    device_index = -1
    device_count = pyaudio_client.get_device_count()
    print(f"Device count: {device_count}")
    print("Devices:")
    for i in range(device_count):
        device_info = pyaudio_client.get_device_info_by_host_api_device_index(0, i)
        print(device_info["name"])
        if DEVICE_NAME in device_info["name"]:
            device_index = i
    if device_index == -1:
        raise Exception("No device found")
    else:
        print(f"Selected Device: {device_index} - {DEVICE_NAME}")
    return device_index
