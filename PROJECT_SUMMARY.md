# Telegram Video Download Bot - Project Summary

## Project Overview

This is a Telegram bot that allows users to download videos from various platforms by simply sending a video URL to the bot. The bot processes the request, downloads the video using yt-dlp, and sends it back to the user via Telegram.

## Key Features

1. **Multi-platform Support**: Downloads videos from YouTube, Vimeo, Twitter, Instagram, TikTok, and thousands of other sites
2. **Telegram Integration**: Seamless integration with Telegram messaging platform
3. **User-friendly Interface**: Simple commands and progress updates
4. **Size and Duration Limits**: Enforces limits to comply with Telegram restrictions
5. **Error Handling**: Comprehensive error handling for various scenarios
6. **Custom Error Messages**: Specific error messages for unsupported sites like Mover.uz

## Technology Stack

- **Python 3.9+**: Main programming language
- **python-telegram-bot**: Telegram Bot API wrapper
- **yt-dlp**: Video downloading library
- **python-dotenv**: Environment variable management

## Project Structure

```
telegram_video_bot/
├── src/
│   └── bot.py              # Main bot logic
├── .env.example           # Environment configuration template
├── .gitignore             # Git ignore rules
├── DEPLOYMENT.md          # Deployment instructions
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── run_bot.py             # Bot execution script
├── setup_bot.py           # Bot setup script
├── test_bot.py            # Bot testing script
├── deploy.py              # Automated deployment script
└── deploy.ps1             # PowerShell deployment script
```

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd telegram_video_bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**:
   - Copy `.env.example` to `.env`
   - Replace `YOUR_BOT_TOKEN_HERE` with your actual Telegram bot token

4. **Run the bot**:
   ```bash
   python run_bot.py
   ```

## Usage

1. Start a conversation with your bot on Telegram
2. Send the `/start` command to begin
3. Send any video URL to download it
4. Wait for the bot to process and send back the video

## Supported Platforms

The bot supports downloading from all platforms supported by yt-dlp, including:
- YouTube
- Vimeo
- Twitter
- Instagram
- TikTok
- And thousands of other sites

## Limitations

- Videos larger than 50MB cannot be sent via Telegram
- Videos longer than 10 minutes are rejected
- Some sites may block downloading attempts

## Error Handling

The bot includes specific error handling for:
- Unsupported URLs (like Mover.uz)
- Instagram format availability issues
- HTTP 403 errors (access denied)
- General download errors

## Deployment

The project includes multiple deployment options:
- Manual Git commands
- Automated Python deployment script (`deploy.py`)
- PowerShell deployment script (`deploy.ps1`)
- GitHub Actions workflow (in `.github/workflows/`)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

This is an open-source project developed for the community.