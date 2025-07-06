# Setup Guide

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Discord Bot Configuration
# Get your Discord bot token from: https://discord.com/developers/applications
DISCORD_TOKEN=your_discord_bot_token_here

# Brave Search API Configuration
# Get your Brave Search API key from: https://api.search.brave.com/
BRAVE_API_KEY=your_brave_search_api_key_here

# Groq API Configuration
# Get your Groq API key from: https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here
```

## API Key Setup Instructions

### 1. Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under "Token", click "Copy" to copy your bot token
6. Paste it in your `.env` file as `DISCORD_TOKEN`

**Required Bot Permissions:**
- Send Messages
- Read Message History
- Use Slash Commands (if implementing slash commands)

**Required Intents:**
- Message Content Intent (enabled in the bot code)

### 2. Brave Search API Key

1. Visit [Brave Search API](https://api.search.brave.com/)
2. Sign up for a free account
3. Go to your dashboard
4. Generate a new API key
5. Copy the key and paste it in your `.env` file as `BRAVE_API_KEY`

**Free Tier Limits:**
- 10,000 queries per month
- Rate limit: 10 requests per second

### 3. Groq API Key

1. Go to [Groq Console](https://console.groq.com/)
2. Create an account or sign in
3. Navigate to API Keys section
4. Generate a new API key
5. Copy the key and paste it in your `.env` file as `GROQ_API_KEY`

**Groq Features:**
- Fast inference (sub-second responses)
- Multiple model options
- Pay-per-use pricing

## Adding Your Discord Bot to a Server

1. Go to your Discord application in the Developer Portal
2. Go to "OAuth2" → "URL Generator"
3. Select the following scopes:
   - `bot`
   - `applications.commands` (for slash commands)
4. Select the following bot permissions:
   - Send Messages
   - Read Message History
   - Use Slash Commands
5. Copy the generated URL and open it in a browser
6. Select your server and authorize the bot

## Testing Your Setup

1. Run the bot: `python bot.py`
2. You should see: "Logged in as [Bot Name]"
3. In your Discord server, try: `!ask What events are coming up?`
4. The bot should respond with event information

## Troubleshooting

### Bot Not Responding
- Check that the bot is online in your server
- Verify the bot has the correct permissions
- Ensure Message Content Intent is enabled

### API Errors
- Double-check all API keys are correct
- Verify you haven't exceeded rate limits
- Check your internet connection

### No Event Data
- Verify the Meetup URL in your configuration
- Check that the group has public events
- Review the console logs for error messages 