import sounddevice as sd
import soundfile as sf
import threading


class SoundPlayer:
    def __init__(self, sound_path):
        self.sound_data, self.sample_rate = sf.read(sound_path)
        self.stream = None

    def play(self):
        sd.play(self.sound_data, self.sample_rate)
        sd.wait()

    def play_async(self):
        thread = threading.Thread(target=self.play)
        thread.start()

    def is_playing(self):
        return self.stream is not None

    def stop(self):
        pass
