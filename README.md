# Spy Game Telegram Bot

## Overview
A Telegram bot for playing the spy game with friends. Players are assigned roles (spy or civilian) with themed cards.

## Project Structure
- `bot.py` - Main bot logic with Telegram handlers
- `cr/` - Clash Royale themed card images
- `jjs/` - JJS themed card images  
- `spy/` - Spy role images

## Configuration
- **BOT_TOKEN**: Set via `BOT_TOKEN` environment variable for security

## Running the Bot
The bot runs via the "Telegram Bot" workflow using `python bot.py`

## Game Themes
1. **Өзімізғо** - Custom text-only cards
2. **JJS** - Jujutsu Shenanigans themed cards with images
3. **Clash Royale** - Clash Royale cards with images

## Scenarios
- Classic - Standard spy game
- Random - Randomly picks special scenarios
- All Spies / All Civilians / Chaos / Opposite - Special game modes
