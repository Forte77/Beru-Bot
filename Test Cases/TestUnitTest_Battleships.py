"""Unittest casses for Battles"""

import pytest
import discord.ext.test as dpytest #discord.ext.test, acts as a "discord server"
from Beru import bot # Import your actual bot object

@pytest.mark.asyncio
async def test_ping_command():
    # 1. Setup the "Fake" Discord world
    await dpytest.empty_config()
    dpytest.configure(bot)

    # 2. Mimic a user typing "!ping"
    await dpytest.message("!ping")

    # 3. Assert (Prove) the bot replied correctly
    assert dpytest.verify().message().content("Pong!")