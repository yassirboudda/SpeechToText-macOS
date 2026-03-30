# SpeechToText — macOS

Voxtral-powered speech-to-text that lives in your macOS menu bar.

Record speech, get instant transcription via Mistral's Voxtral API, and have it automatically typed at your cursor or copied to clipboard.

## Download & Install (No Python Required)

> **Go to the [Releases page](https://github.com/bouddahami/SpeechToText-macOS/releases/latest) and download `SpeechToText.dmg`**

### Quick start

1. Download **`SpeechToText.dmg`** and open it
2. Drag **SpeechToText** into **Applications**
3. Open **SpeechToText** from Applications
4. **First launch:** macOS will say *"can't be opened because it is from an unidentified developer"* — this is normal (no code signing certificate). Fix:
   - Right-click the app → **Open** → click **Open** again
   - Or: **System Settings → Privacy & Security → Open Anyway**
5. The app appears in the **menu bar** (top of screen, near the clock)
6. Click the 🎙 icon → **Add API Key**
7. Get a free API key from [console.mistral.ai](https://console.mistral.ai/) (create an account, go to API Keys)
8. Paste your key, click **Test Key**, then **Save**
9. Click 🎙 → **Start Recording** → speak → **Stop Recording**
10. Your transcription is automatically typed where your cursor is!

## Features

- **Menu bar app** — lives in the macOS menu bar, no Dock icon
- **Record & transcribe** — one click to record, auto-transcribes when you stop
- **Auto type at cursor** — transcription is automatically pasted where your cursor is (configurable)
- **Auto copy to clipboard** — transcription is always copied to clipboard
- **Visual editor** — optional floating editor to view/edit transcription
- **API key management** — add/test/manage your Mistral API key from Settings
- **2-minute recording limit** — optimized for Mistral's free tier

## Permissions

macOS will ask for **Microphone** and **Accessibility** (for type-at-cursor) permissions. Grant both for full functionality.

## Install from Source (for developers)

<details>
<summary>Click to expand developer instructions</summary>

### Requirements

- macOS 10.15+
- Python 3.9+
- A [Mistral API key](https://console.mistral.ai/)

### Installation

```bash
git clone https://github.com/bouddahami/SpeechToText-macOS.git
cd SpeechToText-macOS
pip3 install -r requirements.txt
pip3 install .
```

### Usage

```bash
speechtotext
```

### Build the .app yourself

```bash
pip3 install py2app
python setup_app.py py2app
# Output: dist/SpeechToText.app
```

</details>

## Auto-start on Login

1. Open **System Settings → General → Login Items**
2. Click **+** and select **SpeechToText** from Applications

## Configuration

Config is stored at `~/Library/Application Support/SpeechToText/config.json`.

## Other Platforms

- [Linux version](https://github.com/bouddahami/SpeechToText-Linux)
- [Windows version](https://github.com/bouddahami/SpeechToText-Windows)
