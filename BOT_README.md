# FreeAPIRadar Telegram Bot

Push alerts when free AI API statuses change.

## Setup

### 1. Create bot with @BotFather

1. Open Telegram, find `@BotFather`
2. Send `/newbot`
3. Name: `FreeAPIRadar` (or any name)
4. Username: `freeapiradar_bot` (must be unique, try variations)
5. Copy the token

### 2. Set environment variable

```bash
export TELEGRAM_BOT_TOKEN="your-token-here"
```

### 3. Install dependencies

```bash
pip install python-telegram-bot aiohttp
```

### 4. Run the bot

```bash
# From the freeapiradar repo root:
python -m bot
```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/status` | Current status of all providers |
| `/subscribe groq` | Get alerts when Groq status changes |
| `/subscribe all` | Subscribe to all providers |
| `/unsubscribe groq` | Stop alerts for Groq |
| `/mysubs` | Show your subscriptions |
| `/providers` | List available provider IDs |

## GitHub Actions Integration

The bot sends push alerts automatically when the monitor workflow runs.

Add `TELEGRAM_BOT_TOKEN` to GitHub repo secrets:
- Go to `Settings → Secrets → Actions → New repository secret`
- Name: `TELEGRAM_BOT_TOKEN`
- Value: your bot token

## Architecture

```
bot/
├── __init__.py
├── __main__.py      # python -m bot entry point
├── main.py          # Bot setup, polling mode
├── config.py        # Configuration from env vars
├── handlers.py      # /status, /subscribe, etc.
├── storage.py       # Subscriber persistence (JSON)
└── notifier.py      # Push alerts (called from CI)
```

## Running modes

**Polling mode** (for development or VPS):
```bash
python -m bot
```
Bot runs continuously, responds to commands.

**Notification only** (for GitHub Actions):
```bash
python -m bot.notifier
```
Sends alerts for detected changes, then exits.

## License

AGPL-3.0-only — Copyright (c) 2026 Quorbit Labs
