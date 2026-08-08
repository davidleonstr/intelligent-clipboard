<div align="center">
  <img src="./app/resources/icons/app-icon.svg" alt="icon" width="180"/>
  <br/>
  
  <h3>Application to make your clipboard intelligent using AI</h3>

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

</div>

# IC — Intelligent Clipboard

IC is a lightweight desktop application that enhances your clipboard workflow with AI-powered text processing. By listening for a configurable keyboard shortcut, IC captures your clipboard content, sends it to an AI language model, and replaces it with the model's response — all without interrupting your work.

## Overview

IC runs silently in the background as a frameless desktop window built on PyQt6. When activated, it intercepts the current clipboard content, processes it through the AI API using a predefined system prompt, and writes the result back to the clipboard — ready to paste wherever needed.

The application is designed for precision tasks that benefit from consistent, prompt-driven AI assistance: rephrasing, formatting, summarizing, or transforming text on demand.

## Features

- Hotkey-activated clipboard processing via the AI API
- Support for multiple hotkey combinations, each mapped to its own custom system prompt file
- Functional with all OpenAI-compatible API endpoints (defaults to Google Generative Language API)
- Animated splash loading screen with PyQt/WebChannel bridge
- Secure local storage of the API key using a seed-based XOR cipher
- Model selection from all AI models that support content generation
- Frameless, resizable window with a custom title bar (maximize disabled)
- System tray support — minimizes to tray with Open/Close context menu
- Screen-based navigation: Setup, Home, Help, Error, and Loading screens
- Built-in Help screen with step-by-step usage guide, hotkey reference, and documentation
- Complete configuration system.
- Notification system for user feedback on key actions
- Internationalization (i18n) support via locale files with automatic fallback to English
- Concurrent request protection — simultaneous hotkey triggers are safely blocked

## Requirements

- Python `3.10` or higher

Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

1. Launch the application by running:

```bash
python main.py
```

2. On first launch, an animated splash screen will appear briefly, followed by the setup screen. Enter a valid AI API key.

3. The key is validated against the pattern defined in `app/settings/ic.json`, encrypted with the seed cipher in `app/settings/auth.json`, and stored locally in `app/settings/ic.json`.

4. Once confirmed, the application navigates to the home screen automatically.

## Usage

From the home screen:

- A model selector lists all available AI models that support content generation.
- The listener toggle enables or disables hotkey processing.
- When the listener is active, pressing any configured hotkey reads the current clipboard, sends it to AI using that hotkey's own prompt, and writes the response back to the clipboard. Concurrent requests are blocked — triggering a hotkey while a request is already in progress has no effect.
- The key can be deleted at any time, returning the application to the setup screen.
- The Help button opens the built-in guide with a full usage walkthrough, hotkey reference, and documentation.
- The settings button opens all application settings.
- Minimizing the window sends the application to the system tray. It can be restored via the tray icon or its context menu.

## Configuration

Application settings are loaded through `app/settings/settings.py` (the `SETTINGS` singleton), which reads a set of JSON files under `app/settings/`. File paths are resolved via `app/tree/folders.py`, which builds a lookup table from the glob patterns defined in `app/tree/folders.json`.

### Settings files (`app/settings/`)

| File | Purpose | Keys |
|---|---|---|
| `ic.json` | Core app/API settings | `ic-key` (encrypted API key, `null` until set), `ic-openai-wrapper` (OpenAI-compatible endpoint, defaults to Google's Generative Language API), `ic-key-pattern` (regex used to validate a key before it's accepted) |
| `auth.json` | Cipher configuration | `seed-chiper` (seed string used to derive the XOR keystream for encrypting the stored API key) |
| `gui.json` | Interface settings | `language` (active locale, e.g. `en`) |
| `hotkeys.json` | Hotkey → prompt mapping | one entry per hotkey combination, mapping to a filename under `app/settings/prompts/` |

Editing any of these files directly (while the app is closed) takes effect on the next launch. The API key and cipher seed are the only sensitive values — see [Security](#security).

### Window and screen configs (`app/configs/`)

| File | Purpose |
|---|---|
| `app/configs/windows/app.json` | Window chrome: stylesheet (`style`), background color, icon, and initial `geometry` (x, y, width, height) |

### Hotkeys and prompts

Hotkey combinations are defined in `app/settings/hotkeys.json` as a dictionary, where each key is a hotkey combination (e.g. `'ctrl+i'`) and each value is the filename of a prompt stored under `app/settings/prompts/`:

```json
{
    "ctrl+i": "main.md",
    "ctrl+shift+t": "translate.md"
}
```

You can add as many hotkey → prompt mappings as you like. On startup, `SETTINGS.getHotkeys()` reads each referenced file and loads its contents as the system prompt used for that hotkey's requests. Pressing a hotkey while the listener is enabled sends the current clipboard content to the AI model along with that hotkey's specific prompt, then replaces the clipboard with the response.

### Advanced settings

From the **Settings** screen, under **Advanced**, you can edit:

- **AI API endpoint** (`ic-openai-wrapper`) — the OpenAI-compatible base URL IC sends requests to.
- **API key pattern** (`ic-key-pattern`) — the regex used to validate a key on the setup screen before it's accepted.
- **Seed cipher** (`seed-chiper`) — the seed used to encrypt/decrypt your locally stored API key.

Changes made here are saved to `app/settings/ic.json` and `app/settings/auth.json` respectively and take effect immediately.

> Changing the seed cipher re-derives the encryption keystream. If you already have a saved API key, changing the seed without re-saving the key may make it undecryptable on next launch — re-enter your API key after changing the seed.

### Internationalization

UI strings are loaded from locale files under `app/locales/<language>/`. The active language is set via the `language` field in `app/settings/gui.json`. Missing keys in the selected language fall back automatically to English (`en`).

## Security

The API key is encrypted at rest using a deterministic XOR cipher seeded with a fixed application string. This prevents casual inspection of stored credentials. The key is only decrypted in memory at startup and is never written in plaintext to disk.

This cipher is not cryptographically strong and is intended as obfuscation, not secure key storage.