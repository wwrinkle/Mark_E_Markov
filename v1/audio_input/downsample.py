from core.const import RATE
import librosa


def downsample(chunk, divisor=4):
    downsampled_rate = int(RATE / divisor)
    return [
        downsampled_rate,
        librosa.resample(
            chunk.astype("float32"), orig_sr=RATE, target_sr=downsampled_rate
        ),
    ]
