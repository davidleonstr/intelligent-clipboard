<img src="resources/icons/app-icon.svg" alt="icon" width="180"/>
<br/>

# IC — Intelligent Clipboard

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

IC is a lightweight desktop application that enhances your clipboard workflow with AI-powered text processing. By listening for a configurable keyboard shortcut, IC captures your clipboard content, sends it to a AI language model, and replaces it with the model's response — all without interrupting your work.

## Overview

IC runs silently in the background as a frameless desktop window built on PyQt6. When activated, it intercepts the current clipboard content, processes it through the AI API using a predefined system prompt, and writes the result back to the clipboard — ready to paste wherever needed.

The application is designed for precision tasks that benefit from consistent, prompt-driven AI assistance: rephrasing, formatting, summarizing, or transforming text on demand.

## Features

- Hotkey-activated clipboard processing via the AI API
- Functional with all OpenAI-compatible API endpoints
- Secure local storage of the API key using a seed-based XOR cipher
- Model selection from all AI models that support content generation
- Frameless, resizable window with a custom title bar
- Screen-based navigation between setup and home views
- Notification system for user feedback on key actions

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

2. On first launch, the setup screen will appear. Enter a valid AI API key.

3. The key is validated against the pattern defined in `relatives.json`, encrypted with the seed cipher, and stored locally.

4. Once confirmed, the application navigates to the home screen automatically.

## Usage

From the home screen:

- The stored API key is displayed in masked form and can be copied to the clipboard.
- A model selector lists all available AI models that support content generation.
- The listener toggle enables or disables hotkey processing.
- When the listener is active and the configured hotkey is pressed, IC reads the current clipboard, sends it to AI with the configured system prompt, and writes the response back to the clipboard.
- The key can be deleted at any time, returning the application to the setup screen.

## Configuration

Application behavior is driven by JSON configuration files resolved through `config/config.json`. Key runtime values — including the hotkey combination, API key pattern, prompt file path, artificial intelligence API endpoint, and cipher seed — are defined in `app/relatives.json`.

The system prompt used for AI processing is loaded from the file path specified in `relatives.json` and sent automatically with every clipboard request.

## Security

The API key is encrypted at rest using a deterministic XOR cipher seeded with a fixed application string. This prevents casual inspection of stored credentials. The key is only decrypted in memory at startup and is never written in plaintext to disk.

This cipher is not cryptographically strong and is intended as obfuscation, not secure key storage. For higher-security environments, consider replacing `SeedCipher` with an OS-level keychain integration.