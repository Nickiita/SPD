import sounddevice as sd
import soundfile as sf


class SoundPlayer:
    def __init__(self, sound_path):
        self.sound_data, self.sample_rate = sf.read(sound_path)

    def play(self):
        sd.play(self.sound_data, self.sample_rate)
        sd.wait()
