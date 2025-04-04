from const import DEVICE_NAME
from logger import log


def get_device_index(pyaudio_client):
    device_index = -1
    device_count = pyaudio_client.get_device_count()
    for i in range(device_count):
        device_info = pyaudio_client.get_device_info_by_host_api_device_index(0, i)
        if DEVICE_NAME in device_info["name"]:
            device_index = i
            log("SELECTED DEVICE INFO:", device_info)
            break
    if device_index == -1:
        raise Exception("No device found")
    return device_index
