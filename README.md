# Monsieur-Self

A powerful and multi-functional Telegram user-bot. Automates profile updates (bio, name, clock-pfp), adds fun text modes, provides an AFK system, and integrates Google's Gemini AI for `.ask` commands. Includes an inline helper-bot panel for easy management.

---

### ⚠️ Disclaimer

**Using a Telegram user-bot (self-bot) is a violation of Telegram's Terms of Service.**

Running this code gives you powerful automation tools, but it also accesses your account through the Telegram API in a way that is not intended for normal users. Telegram can detect this activity, and using a self-bot **can result in your account being temporarily or permanently banned.**

The creator of this repository is not responsible for any damage or consequences that may arise from your use of this code.

**Use this at your own risk.**

---

## ✨ Features

* **Profile Automation**: Automatically update your last name, bio, and profile picture with a running clock.
* **Gemini AI**: Use the `.ask` command to get answers from Google's Gemini AI.
* **AFK Mode**: Automatically reply to DMs and mentions when you are away.
* **Notes System**: Save and retrieve notes quickly with `#keyword`.
* **Text Modes**: Apply fun formatting to your outgoing messages (bold, italic, reverse, etc.).
* **Crush/Enemy Lists**: Auto-react to messages from "crush" users and auto-delete DMs from "enemy" users.
* **Utility Commands**: Includes tools like `.info`, `.status`, `.translate`, `.googleplay`, and many more.
* **Helper Panel**: A `panel` command to open an inline keyboard for easy control of your bot's features.

## ⚙️ 1. Setup & Configuration

You will need several API keys and IDs to set up this bot.

1.  **Fork & Clone**: First, fork this repository and then clone it to your server or local machine.
    ```bash
    git clone [https://github.com/erm-iya/monsieur-self.git](https://github.com/YOUR_USERNAME/monsieur-self.git)
    cd monsieur-self
    ```

2.  **Get Telegram API Keys**:
    * Go to [my.telegram.org](https://my.telegram.org) and log in.
    * Click on "API development tools" and create a new application.
    * You will get your `API_ID` and `API_HASH`.

3.  **Create Your Helper Bot**:
    * Talk to [@BotFather](https://t.me/BotFather) on Telegram.
    * Use the `/newbot` command to create a new bot.
    * Save the **`BOT_TOKEN`** he gives you.
    * Use the `/setinline` command, select your new bot, and set its inline placeholder text to something like "Helper Panel".

4.  **Get Your User ID**:
    * Talk to [@userinfobot](https://t.me/userinfobot) and copy your user ID. This will be your `ADMIN_USERS`.

5.  **(Optional) Get Gemini AI Key**:
    * Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
    * Create a new API key. This will be your `GEMINI_API_KEY`.

6.  **(Optional) Create Log Channel**:
    * Create a new **private channel** on Telegram.
    * Add [@userinfobot](https://t.me/userinfobot) to the channel as an admin to get the channel's ID.
    * Copy the Channel ID (it will look like `-100123...`). This is your `LOG_CHANNEL_ID`.
    * You can now kick the bot.

7.  **Fill `config.py`**:
    * Open the `config.py` file and fill in all the values you just collected.

    ```python
    # Example config.py
    API_ID = 1234567
    API_HASH = "a1b2c3d4e5f6..."
    
    BOT_TOKEN = "123456:ABCDEFGHIJK..."
    
    ADMIN_USERS = [987654321] # Put your user ID here
    
    GEMINI_API_KEY = "AIzaSy..." # Optional
    
    LOG_CHANNEL_ID = -100123456789 # Optional
    ```

## 📦 2. Installation

1.  **Install Python & Git**: Make sure you have `python3` and `git` installed on your system.

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 3. How to Run

You need to run **both** the user-bot and the helper-bot simultaneously. A `screen` or `tmux` session is highly recommended for running them 24/7.

### A. Running the Helper Bot (`helper.py`)

This Flask app must be running and accessible via a public URL for Telegram to send it updates.

1.  **Run the helper app**:
    ```bash
    python3 helper.py
    ```
    By default, this runs on port 80. You may need to use `sudo` or configure a reverse proxy (like Nginx) to run on this port.

2.  **Set the Webhook**:
    * You need a public domain or IP address (e.g., `https://your.domain.com`).
    * Take your `BOT_TOKEN` and your public URL and run this command in your browser or a terminal (replace the all-caps values):
    ```bash
    curl "[https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook?url=https://YOUR.DOMAIN.COM/helper](https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook?url=https://YOUR.DOMAIN.COM/helper)"
    ```
    * If successful, you will see `{"ok":true,"result":true,"description":"Webhook was set"}`.

### B. Running the User-Bot (`self.py`)

1.  **Run the main bot**:
    ```bash
    python3 self.py
    ```

2.  **First-Time Login**:
    * The first time you run this, Telethon will ask you for your phone number, the code Telegram sends you, and your 2FA password (if you have one).
    * It will create a `self.session` file. **DO NOT** share this file with anyone; it gives them full access to your account.
    * After logging in, the bot will restart and be fully operational.

## 📋 4. Commands

### Main Commands
| Command | Description |
| :--- | :--- |
| `.help` / `راهنما` | Shows the full list of commands and current settings. |
| `panel` / `پنل` | Opens the inline helper panel (via the helper bot). |
| `xo` / `دوز` | Starts a Tic-Tac-Toe game (via the helper bot). |
| `.restart` / `ریستارت` | Restarts the user-bot. |

### AI & Automation
| Command | Description |
| :--- | :--- |
| `.ask <prompt>` | Ask a question to Google's Gemini AI. |
| `.afk <reason>` | Enables AFK mode with an optional reason. |
| `.timeprofile on/off`| Toggles the automatic clock profile picture. |
| `.timename on/off` | Toggles the automatic clock in your last name. |
| `.timebio on/off` | Toggles the automatic clock in your bio. |
| `.timecrush on/off` | Toggles sending a message to your crush list on the hour. |

### Notes System
| Command | Description |
| :--- | :--- |
| `.save <key> <text>` | Saves a note. (Also works by replying). |
| `#<key>` | Retrieves and sends the note. |
| `.notes` / `.listnotes` | Lists all saved note keywords. |
| `.delnote <key>` | Deletes a saved note. |

### Utility & Tools
| Command | Description |
| :--- | :--- |
| `.info` (reply/id) | Gets information about a user. |
| `.status` / `وضعیت` | Shows a full status report of your account's chats. |
| `.sessions` | Lists all active Telegram sessions. |
| `.translate` (reply) | Translates a message (defaults to Farsi). |
| `.download` (reply) | Downloads the replied-to media and sends it to your log channel. |
| `.googleplay <query>` | Searches for an app on the Google Play Store. |
| `.checker <phone>` | Checks a phone number using an external API. |
| `.whois <domain>` | Performs a Whois lookup on a domain. |
| `.qrcode <text>` | Generates a QR code from text. |

### Chat Management (Group)
| Command | Description |
| :--- | :--- |
| `tagall` / `تگ` | Tags the 100 most recent users in the chat. |
| `tagadmins` | Tags all admins in the chat. |
| `.clean <num>` | Deletes the last X messages sent by you. |
| `.ban` (reply/id) | Bans a user from the group. |
| `.pin` (reply) | Pins the replied-to message. |
| `.unpin` | Unpins the current message. |
| `report` (reply) | Reports a user to all group admins. |
| `.voicecall <mins>` | Schedules a group voice call for X minutes from now. |

### Text & Fun
| Command | Description |
| :--- | :--- |
| `.spam <text> <count>` | Spams a message X times. |
| `.flood <text> <count>` | Floods a single message X times. |
| `fun <type>` | Runs a fun animation (e.g., `fun love`, `fun star`). |
| `heart` / `قلب` | Sends a "heart" loading animation. |
| `.whisper <text>` (reply) | Sends a whisper message (via @whisperbot). |
| `(text mode) on/off` | Toggles text modes (e.g., `bold on`, `spoiler on`). |
| `(action mode) on/off`| Toggles action modes (e.g., `typing on`, `game on`). |

## 🤝 Contributing

Contributions are welcome! If you have a feature to add or a bug to fix, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/MyNewFeature`).
3.  Commit your changes (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/MyNewFeature`).
5.  Open a Pull Request.
