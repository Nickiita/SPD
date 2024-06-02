import sounddevice as sd
import numpy as np
from pydub import AudioSegment

# Загрузка аудиофайла
audio_file = 'mem.wav'
audio = AudioSegment.from_file(audio_file, format="wav")

# Настройка аудиопотока
RATE = audio.frame_rate
CHANNELS = audio.channels
CHUNK = 1024

# Преобразование аудиофайла в массив numpy
audio_data = np.array(audio.get_array_of_samples())

def callback(outdata, frames, time, status):
    global current_pos
    if current_pos + frames * CHANNELS > len(audio_data):
        current_pos = 0
    outdata[:] = audio_data[current_pos:current_pos + frames * CHANNELS].reshape(-1, CHANNELS)
    current_pos += frames * CHANNELS

current_pos = 0

# Найти индекс устройства Virtual Audio Cable
device_info = sd.query_devices()
vac_device_index = None
for idx, device in enumerate(device_info):
    if 'CABLE Input' in device['name']:
        vac_device_index = idx
        break

if vac_device_index is None:
    raise RuntimeError("Virtual Audio Cable device not found")

# Открытие потока воспроизведения
with sd.OutputStream(samplerate=RATE, channels=CHANNELS, callback=callback, dtype=np.int16, device=vac_device_index):
    print("Streaming audio... Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopped streaming.")