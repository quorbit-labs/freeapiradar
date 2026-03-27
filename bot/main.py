# Copyright (c) 2026 Quorbit Labs
# SPDX-License-Identifier: AGPL-3.0-only

"""FreeAPIRadar Telegram Bot — entry point.

Usage:
    # Set env var:
    export TELEGRAM_BOT_TOKEN="your-bot-token-from-botfather"

    # Run bot (polling mode):
    python -m bot.main

    # Send notifications only (for GitHub Actions):
    python -m bot.notifier
"""

import logging
import sys

from telegram.ext import ApplicationBuilder, CommandHandler

from . import config
from .handlers import (
    cmd_help,
    cmd_mysubs,
    cmd_providers,
    cmd_start,
    cmd_status,
    cmd_subscribe,
    cmd_unsubscribe,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    if not config.BOT_TOKEN:
        logger.error(
            "TELEGRAM_BOT_TOKEN not set!\n"
            "1. Talk to @BotFather on Telegram\n"
            "2. Create a bot: /newbot\n"
            "3. Copy the token\n"
            "4. export TELEGRAM_BOT_TOKEN='your-token'"
        )
        sys.exit(1)

    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("subscribe", cmd_subscribe))
    app.add_handler(CommandHandler("unsubscribe", cmd_unsubscribe))
    app.add_handler(CommandHandler("mysubs", cmd_mysubs))
    app.add_handler(CommandHandler("providers", cmd_providers))

    logger.info("FreeAPIRadar bot starting... (polling mode)")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
