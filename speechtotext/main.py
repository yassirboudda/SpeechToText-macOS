#!/usr/bin/env python3
"""SpeechToText - Voxtral-powered speech transcription for macOS menu bar."""

import sys
import json
import os
import threading
import subprocess
import time

from speechtotext.recorder import AudioRecorder
from speechtotext.transcriber import transcribe, test_api_key

CONFIG_DIR = os.path.expanduser('~/Library/Application Support/SpeechToText')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

DEFAULT_CONFIG = {
    'mistral_api_key': '',
    'auto_type_at_cursor': True,
}


def load_config():
    """Load configuration from config file."""
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return dict(DEFAULT_CONFIG)

    with open(CONFIG_FILE) as f:
        stored = json.load(f)
    config = dict(DEFAULT_CONFIG)
    config.update(stored)
    return config


def save_config(config):
    """Save configuration to config file."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def copy_to_clipboard(text):
    """Copy text to macOS clipboard."""
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))


def paste_at_cursor():
    """Simulate Cmd+V on macOS."""
    script = 'tell application "System Events" to keystroke "v" using command down'
    subprocess.run(['osascript', '-e', script], timeout=5, check=False)


class SpeechToTextApp:
    """Menu bar speech-to-text app for macOS using rumps."""

    PREVIEW_LEN = 60

    def __init__(self, config):
        import rumps
        self.rumps = rumps
        self.config = config
        self.api_key = config.get('mistral_api_key', '')
        self.auto_type = config.get('auto_type_at_cursor', True)
        self.recorder = AudioRecorder()
        self.is_recording = False
        self.is_transcribing = False
        self.transcription = ''

        self.app = rumps.App('SpeechToText', title='🎙', quit_button=None)
        self._build_menu()
        self.app.run()

    def _build_menu(self):
        rumps = self.rumps
        self.app.menu.clear()

        if not self.api_key:
            self.app.menu = [
                rumps.MenuItem('🔑  Add API Key', callback=self._on_settings),
                None,
                rumps.MenuItem('Quit', callback=self._on_quit),
            ]
            return

        self.record_item = rumps.MenuItem('🎙  Start Recording', callback=self._on_record)
        self.status_item = rumps.MenuItem('Ready')
        self.status_item.set_callback(None)
        self.text_item = rumps.MenuItem('No transcription yet')
        self.text_item.set_callback(None)
        self.copy_item = rumps.MenuItem('📋  Copy to Clipboard', callback=self._on_copy)
        self.type_item = rumps.MenuItem('⌨  Type at Cursor', callback=self._on_type)
        self.delete_item = rumps.MenuItem('🗑  Delete Transcription', callback=self._on_delete)
        self.editor_item = rumps.MenuItem('📝  Visual Editor', callback=self._on_editor)
        self.settings_item = rumps.MenuItem('⚙  Settings', callback=self._on_settings)

        self.app.menu = [
            self.record_item,
            self.status_item,
            None,
            self.text_item,
            None,
            self.copy_item,
            self.type_item,
            self.delete_item,
            None,
            self.editor_item,
            self.settings_item,
            None,
            rumps.MenuItem('Quit', callback=self._on_quit),
        ]

    def _update_status(self, text):
        if hasattr(self, 'status_item'):
            self.status_item.title = text

    def _update_text_preview(self):
        if not hasattr(self, 'text_item'):
            return
        if self.transcription.strip():
            preview = self.transcription.replace('\n', ' ')
            if len(preview) > self.PREVIEW_LEN:
                preview = preview[:self.PREVIEW_LEN] + '…'
            self.text_item.title = preview
        else:
            self.text_item.title = 'No transcription yet'

    # ── Handlers ──

    def _on_record(self, sender):
        if self.is_transcribing:
            return
        if self.is_recording:
            self._stop_recording()
        else:
            self._start_recording()

    def _start_recording(self):
        try:
            self.recorder.start(
                on_duration_update=self._on_tick,
                on_max_reached=self._on_max,
            )
            self.is_recording = True
            self.record_item.title = '⏹  Stop Recording'
            self._update_status('Recording…')
        except Exception as e:
            self._update_status(f'Error: {e}')

    def _stop_recording(self):
        filepath = self.recorder.stop()
        self.is_recording = False
        self.record_item.title = '🎙  Start Recording'

        if filepath:
            self.is_transcribing = True
            self.record_item.title = '⏳  Transcribing…'
            self._update_status('Transcribing…')
            t = threading.Thread(target=self._transcribe_bg, args=(filepath,), daemon=True)
            t.start()

    def _on_tick(self, seconds):
        dur = self.recorder.format_duration(seconds)
        self.record_item.title = f'⏹  Stop Recording  ({dur})'

    def _on_max(self):
        self._stop_recording()

    def _transcribe_bg(self, filepath):
        try:
            text = transcribe(filepath, self.api_key)
            self._on_transcribe_ok(text)
        except Exception as e:
            self._on_transcribe_err(str(e))
        finally:
            self.recorder.cleanup()

    def _on_transcribe_ok(self, text):
        self.is_transcribing = False
        self.record_item.title = '🎙  Start Recording'
        if text:
            if self.transcription.strip():
                self.transcription += '\n' + text
            else:
                self.transcription = text
            copy_to_clipboard(self.transcription.strip())
            if self.auto_type:
                self._update_status('✓ Typing at cursor…')
                time.sleep(0.7)
                paste_at_cursor()
            else:
                self._update_status('✓ Copied to clipboard – ready to paste')
        else:
            self._update_status('No speech detected')
        self._update_text_preview()

    def _on_transcribe_err(self, error):
        self.is_transcribing = False
        self.record_item.title = '🎙  Start Recording'
        self._update_status(f'Error: {error}')

    def _on_copy(self, sender):
        text = self.transcription.strip()
        if text:
            copy_to_clipboard(text)
            self._update_status('Copied to clipboard!')

    def _on_type(self, sender):
        text = self.transcription.strip()
        if not text:
            return
        copy_to_clipboard(text)
        threading.Thread(target=self._delayed_paste, daemon=True).start()

    def _delayed_paste(self):
        time.sleep(0.7)
        paste_at_cursor()

    def _on_delete(self, sender):
        self.transcription = ''
        self._update_status('Transcription deleted')
        self._update_text_preview()

    def _on_editor(self, sender):
        from speechtotext.editor import show_editor
        show_editor(self)

    def _on_settings(self, sender):
        from speechtotext.settings import show_settings
        show_settings(self)

    def _on_quit(self, sender):
        self.rumps.quit_application()

    def apply_settings(self, new_api_key, new_auto_type):
        """Apply changed settings."""
        key_changed = new_api_key != self.api_key
        self.api_key = new_api_key
        self.auto_type = new_auto_type
        self.config['mistral_api_key'] = new_api_key
        self.config['auto_type_at_cursor'] = new_auto_type
        save_config(self.config)
        if key_changed:
            self._build_menu()

    def update_transcription_from_editor(self, text):
        self.transcription = text
        self._update_text_preview()


def main():
    """Main entry point."""
    config = load_config()
    SpeechToTextApp(config)


if __name__ == '__main__':
    main()
