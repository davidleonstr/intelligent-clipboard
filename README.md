<div align="center">
  <img src="resources/icons/app-icon.svg" alt="icon" width="180"/>
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
- Functional with all OpenAI-compatible API endpoints (defaults to Google Generative Language API)
- Animated splash loading screen with PyQt/WebChannel bridge
- Secure local storage of the API key using a seed-based XOR cipher
- Model selection from all AI models that support content generation
- Frameless, resizable window with a custom title bar (maximize disabled)
- System tray support — minimizes to tray with Open/Close context menu
- Screen-based navigation: Setup, Home, Help, Error, and Loading screens
- Built-in Help screen with step-by-step usage guide and hotkey reference
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

3. The key is validated against the pattern defined in `relatives.json`, encrypted with the seed cipher, and stored locally.

4. Once confirmed, the application navigates to the home screen automatically.

## Usage

From the home screen:

- A model selector lists all available AI models that support content generation.
- The listener toggle enables or disables hotkey processing.
- When the listener is active and the configured hotkey is pressed, IC reads the current clipboard, sends it to AI with the configured system prompt, and writes the response back to the clipboard. Concurrent requests are blocked — triggering the hotkey while a request is already in progress has no effect.
- The key can be deleted at any time, returning the application to the setup screen.
- The Help button opens the built-in guide with a full usage walkthrough and hotkey reference.
- Minimizing the window sends the application to the system tray. It can be restored via the tray icon or its context menu.

## Configuration

Application behavior is driven by JSON configuration files resolved through `config/config.json`. Key runtime values — including the hotkey combination, API key pattern, prompt file path, AI API endpoint, and cipher seed — are defined in `app/relatives.json`.

The system prompt used for AI processing is loaded from the file path specified in `relatives.json` and sent automatically with every clipboard request.

### Internationalization

UI strings are loaded from locale files under `locales/<language>/`. The active language is set via the `gui.language` field in `relatives.json`. Missing keys in the selected language fall back automatically to English (`en`).

## Security

The API key is encrypted at rest using a deterministic XOR cipher seeded with a fixed application string. This prevents casual inspection of stored credentials. The key is only decrypted in memory at startup and is never written in plaintext to disk.

This cipher is not cryptographically strong and is intended as obfuscation, not secure key storage.