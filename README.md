# SpeechToText — macOS

Voxtral-powered speech-to-text that lives in your macOS menu bar.

Record speech, get instant transcription via Mistral's Voxtral API, and have it automatically typed at your cursor or copied to clipboard.

## Features

- **Menu bar app** — lives in the macOS menu bar, no Dock icon
- **Record & transcribe** — one click to record, auto-transcribes when you stop
- **Auto type at cursor** — transcription is automatically pasted where your cursor is (configurable)
- **Auto copy to clipboard** — transcription is always copied to clipboard
- **Visual editor** — optional floating editor to view/edit transcription
- **API key management** — add/test/manage your Mistral API key from Settings
- **2-minute recording limit** — optimized for Mistral's free tier

## Requirements

- macOS 10.15+
- Python 3.9+
- A [Mistral API key](https://console.mistral.ai/)

## Installation

```bash
# Clone the repo
git clone https://github.com/bouddahami/SpeechToText-macOS.git
cd SpeechToText-macOS

# Install dependencies
pip3 install -r requirements.txt

# Install the app
pip3 install .
```

## Usage

```bash
speechtotext
```

On first launch, you'll see only "🔑 Add API Key" in the menu bar dropdown. Click it to enter and test your Mistral API key.

## Auto-start on Login

1. Open **System Preferences → Users & Groups → Login Items**
2. Click **+** and add the `speechtotext` script (usually `~/.local/bin/speechtotext` or find it with `which speechtotext`)

Or create a Launch Agent:

```bash
cat > ~/Library/LaunchAgents/com.speechtotext.app.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.speechtotext.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/speechtotext</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.speechtotext.app.plist
```

## Configuration

Config is stored at `~/Library/Application Support/SpeechToText/config.json`.

## Permissions

macOS will ask for **Microphone** and **Accessibility** (for type-at-cursor) permissions. Grant both for full functionality.

## Other Platforms

- [Linux version](https://github.com/bouddahami/SpeechToText)
- [Windows version](https://github.com/bouddahami/SpeechToText-Windows)
