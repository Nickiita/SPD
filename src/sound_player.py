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
        self.playing = False

    def adjust_volume(self, data, volume):
        return data * volume

    def play(self):
        try:
            self.stream = sd.OutputStream(samplerate=self.sample_rate, channels=len(self.sound_data.shape))
            self.stream.start()
            self.playing = True
            sd.play(self.sound_data, self.sample_rate)
            sd.wait()

        finally:
            if self.stream is not None:
                self.stream.stop()
                self.stream.close()
            self.playing = False
            self.stream = None

    def play_async(self):
        thread = threading.Thread(target=self.play)
        thread.start()

    def is_playing(self):
        return self.playing

    def stop(self):
        self.playing = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
        sd.stop()
        self.stream = None
