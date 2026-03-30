"""py2app setup for SpeechToText macOS app."""

from setuptools import setup

APP = ['speechtotext/__main__.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'assets/icon.icns',
    'plist': {
        'CFBundleName': 'SpeechToText',
        'CFBundleDisplayName': 'SpeechToText',
        'CFBundleIdentifier': 'com.bouddahami.speechtotext',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.15',
        'LSUIElement': True,  # Hide from Dock (menu bar only)
        'NSMicrophoneUsageDescription': 'SpeechToText needs microphone access to record speech for transcription.',
        'NSAppleEventsUsageDescription': 'SpeechToText needs accessibility to type transcriptions at your cursor.',
    },
    'packages': ['speechtotext', 'rumps', 'sounddevice', 'numpy', 'requests'],
    'includes': ['tkinter', 'tkinter.ttk'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
