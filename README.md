# 🤖 ScooVice BOT V2

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.4.0-blue)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-orange)](CHANGELOG.md)

> **Revolutionizing Discord Moderation** – ScooVice BOT V2 is your ultimate companion for maintaining order, fostering community, and automating server management with cutting-edge features and zero downtime.

## 🌟 What's New in v2.0.0 – Major Overhaul!

This is a **groundbreaking major update** that transforms ScooVice BOT from a simple tool into a professional, enterprise-grade moderation platform. Experience lightning-fast responses, robust error handling, and seamless database integration—all designed for servers of any size.

- ⚡ **Zero Interaction Timeouts**: Every command responds instantly with advanced defer/followup technology.
- 🛡️ **Bulletproof Moderation**: Complete suite with auto-warnings, role hierarchy protection, and comprehensive logging.
- 🔧 **Production-Ready**: Global error handlers, database safety, and scalable architecture.
- 🎨 **Modern UI**: Sleek embeds, professional styling, and intuitive commands.

## ✨ Features

### 🛡️ **Advanced Moderation System**

- **Admin Commands**: Kick, ban, tempban, mute, unmute with permission and role checks.
- **Smart Warning System**: Automatic timeout at 3 warnings, with reset and logging.
- **Auto-Moderation**: Real-time detection of banned words, excessive caps, links, and spam.

### 📊 **Intelligent Logging & Analytics**

- **Action Logging**: Every moderation action stored in database with timestamps, reasons, and user details.
- **Transparency**: Embed-based logs for easy review and accountability.

### 🎛️ **Customizable & Extensible**

- **Custom Commands**: Create guild-specific commands stored in database.
- **Database Integration**: MongoDB for persistent storage of warnings, logs, and custom data.
- **Global Error Handling**: Professional responses for all errors, keeping your server clean.

### 🚀 **Performance & Reliability**

- **Async Architecture**: Handles high-traffic servers without lag.
- **Stable Sync**: Global command synchronization prevents duplicates.
- **Zero Crashes**: Comprehensive error catching and graceful failures.

## 📦 Installation

### Prerequisites

- Python 3.13+
- MongoDB Atlas account (free tier available)
- Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))

### Setup Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/ScooVice/scoovice-bot-v2.git
   cd scoovice-bot-v2
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory:

   ```
   DISCORD_TOKEN=your_bot_token_here
   GUILD_ID=your_server_id_here  # Optional, for testing
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
   ```

4. **Run the Bot**:

   ```bash
   python run.py
   ```

5. **Invite to Server**:
   Use the OAuth2 URL from Discord Developer Portal with `bot` and `applications.commands` scopes.

## 🎮 Usage

Once running, ScooVice BOT V2 will automatically sync commands and display "Listening to /help | ScooVice's BOT V2" in its status.

### Command Categories

#### 🛡️ **Moderation Commands**

- `/kick <user> [reason]`: Remove a user from the server.
- `/ban <user> [reason]`: Permanently ban a user.
- `/tempban <user> <duration> [reason]`: Temporarily ban for specified time (e.g., 1d, 2h).
- `/mute <user> [reason]`: Timeout a user (mute).
- `/unmute <user>`: Remove timeout from a user.
- `/warn <user> [reason]`: Issue a warning (auto-mute at 3 warnings).
- `/warnings <user>`: Check a user's warning count.
- `/clearwarnings <user>`: Reset a user's warnings to 0.

#### 🤖 **Utility Commands**

- `/help`: Display all available commands with descriptions.
- `/addcommand <name> <response>`: Add a custom command (admin only).
- `/removecommand <name>`: Remove a custom command (admin only).

#### 🔧 **Auto-Moderation**

- Automatically detects and handles violations in real-time.
- Configurable banned words in `bot/cogs/automod.py`.

## 📋 Requirements

- `discord.py==2.4.0`
- `motor==3.5.1`
- `python-dotenv==1.0.1`

See `requirements.txt` for full list.

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with detailed changes.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📈 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and updates.

## 🚀 Future Updates

Stay tuned for ScooVice BOT v3.0.0, coming soon with exciting new features:

- 🎵 **Music Player**: Full YouTube integration with queue management, playlists, and audio controls.
- 🤖 **AI Chatbot**: Advanced conversational AI powered by Groq for natural interactions.
- 🌍 **Enhanced Multi-Language**: Support for more languages and improved translations.
- 📊 **Analytics Dashboard**: Server statistics and moderation insights.

If you have suggestions or want to report bugs, visit [ScooVice's GitHub](https://github.com/ScooVice)!

---

**Built with ❤️ for the Discord community. Ready to elevate your server moderation to the next level!** 🚀

#ScooViceBOT #DiscordModeration #v2.0.0
