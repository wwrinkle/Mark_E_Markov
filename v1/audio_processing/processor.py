from audio_input.ChunkManager import ChunkManager
from audio_processing.PitchProcessor import PitchProcessor
from audio_processing.audio_file import chunk_to_wav_file
from audio_processing.tempo import get_tempo
from core.const import (
    WRITE_WAV_FILES,
)
from core.profiler import profile


def process_audio():
    chunk_index = 0
    last_tempo = None
    while True:
        try:
            # print('getting chunk')
            chunk_data = ChunkManager().chunks.get_nowait()

            print(f"processing chunk {chunk_index}")
            chunk_start_time = chunk_data[0]
            chunk = chunk_data[1]
            if WRITE_WAV_FILES:
                profile(chunk_to_wav_file)(chunk, chunk_index)

            tempo, last_beat_time = profile(get_tempo)(
                chunk, chunk_start_time, last_tempo=last_tempo
            )
            last_tempo = tempo
            print(f"tempo: {tempo}")
            print(f"last beat: {last_beat_time}")
            pitches = profile(PitchProcessor().process)(chunk)
            print(f"pitches: {pitches}")
            chunk_index += 1
        except:
            # print('no chunk found')
            continue
