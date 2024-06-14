import sounddevice as sd
import soundfile as sf
import threading


class SoundPlayer:
    def __init__(self, sound_path, volume=1.0, playback_speed=1.0):
        self.sound_data, self.sample_rate = sf.read(sound_path)
        self.volume = volume
        self.playback_speed = playback_speed
        self.stream = None
        self.sound_data = self.adjust_volume(self.sound_data, self.volume)
        self.sample_rate = int(self.sample_rate * self.playback_speed)

    def adjust_volume(self, data, volume):
        return data * volume

    def play(self):
        sd.play(self.sound_data, self.sample_rate)
        sd.wait()

    def play_async(self):
        thread = threading.Thread(target=self.play)
        thread.start()

    def is_playing(self):
        return self.stream is not None

    def stop(self):
        sd.stop()
