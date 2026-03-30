"""Audio recording using sounddevice (cross-platform)."""

import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
import threading
import time


class AudioRecorder:
    """Records audio from the microphone and saves to a WAV file."""

    MAX_DURATION = 120  # seconds
    SAMPLE_RATE = 16000
    CHANNELS = 1

    def __init__(self):
        self.recording = False
        self.duration = 0
        self.filepath = None
        self._frames = []
        self._thread = None
        self.on_duration_update = None
        self.on_max_reached = None

    def start(self, on_duration_update=None, on_max_reached=None):
        """Start recording audio."""
        self.on_duration_update = on_duration_update
        self.on_max_reached = on_max_reached
        self._frames = []
        self.duration = 0

        fd, self.filepath = tempfile.mkstemp(suffix='.wav')
        os.close(fd)

        self.recording = True
        self._thread = threading.Thread(target=self._record_loop, daemon=True)
        self._thread.start()

    def _record_loop(self):
        """Record audio in a background thread."""
        try:
            with sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                channels=self.CHANNELS,
                dtype='int16',
                blocksize=self.SAMPLE_RATE,  # 1 second blocks
            ) as stream:
                while self.recording and self.duration < self.MAX_DURATION:
                    data, _ = stream.read(self.SAMPLE_RATE)
                    self._frames.append(data.copy())
                    self.duration += 1
                    if self.on_duration_update:
                        self.on_duration_update(self.duration)
                    if self.duration >= self.MAX_DURATION:
                        if self.on_max_reached:
                            self.on_max_reached()
                        break
        except Exception as e:
            print(f'Recording error: {e}')

    def stop(self):
        """Stop recording and return the path to the WAV file."""
        self.recording = False
        if self._thread:
            self._thread.join(timeout=3)
            self._thread = None

        if self._frames and self.filepath:
            audio_data = np.concatenate(self._frames, axis=0)
            with wave.open(self.filepath, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(2)  # 16-bit = 2 bytes
                wf.setframerate(self.SAMPLE_RATE)
                wf.writeframes(audio_data.tobytes())

        return self.filepath

    def cleanup(self):
        """Remove temp recording file."""
        if self.filepath and os.path.exists(self.filepath):
            os.unlink(self.filepath)
            self.filepath = None

    def format_duration(self, seconds=None):
        """Format seconds as M:SS string."""
        if seconds is None:
            seconds = self.duration
        m = seconds // 60
        s = seconds % 60
        return f'{m}:{s:02d}'
