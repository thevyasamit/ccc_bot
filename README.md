# Discord Meetup Events Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord](https://img.shields.io/badge/Discord-Bot-7289DA.svg)](https://discord.com/developers/docs/intro)
[![Groq](https://img.shields.io/badge/Groq-LLM-00A67E.svg)](https://console.groq.com/)
[![Brave Search](https://img.shields.io/badge/Brave-Search-FF2000.svg)](https://api.search.brave.com/)

A plug-and-play Discord bot that tracks events from any Meetup group and answers questions about upcoming events, group information, and community details. The bot combines data from Meetup events pages and official websites to provide comprehensive information to users.

## Features

- **Multi-Group Support**: Track events from multiple Meetup groups simultaneously
- **Comprehensive Data**: Combines Meetup event data with official website information
- **AI-Powered Responses**: Uses Groq LLM to provide intelligent answers about events
- **Real-time Updates**: Fetches live data from Meetup and official websites
- **Easy Configuration**: Simple dictionary-based configuration for adding new groups
- **Rich Event Details**: Extracts dates, times, locations, descriptions, RSVP counts, and more

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Brave Search API Key
- Groq API Key

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd ccc_bot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Edit .env with your API keys
```

### 3. Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DISCORD_TOKEN=your_discord_bot_token_here
BRAVE_API_KEY=your_brave_search_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Configure Meetup Groups

Edit the `EVENT_GROUPS` dictionary in `bot.py` to add your Meetup groups:

```python
EVENT_GROUPS = {
    "columbus_code_coffee": {
        "name": "Columbus Code & Coffee",
        "meetup_url": "https://www.meetup.com/columbus-code-and-coffee/events/",
        "website_url": "https://cbuscodeandcoffee.com/",
        "description": "Software engineering community for developers by developers"
    },
    # Add more groups here...
}
```

### 5. Run the Bot

```bash
python bot.py
```

## Usage

### Discord Commands

- `!ask <question>` - Ask a question about events and group information
- `/ask <question>` - Alternative command format

### Example Questions

- "When is the next event?"
- "What events are happening this month?"
- "Where does the group meet?"
- "How many members are in the group?"
- "What's the group's description?"
- "Are there any online events?"

## Plug-and-Play Configuration

### Adding New Meetup Groups

1. **Find the Meetup Group URL**: Navigate to the group's events page
2. **Find the Official Website**: Look for the group's official website (optional)
3. **Add Configuration**: Add a new entry to the `EVENT_GROUPS` dictionary


### Switching Between Groups

Change the `DEFAULT_GROUP` constant in `bot.py`:

```python
DEFAULT_GROUP = "python_columbus"  # Switch to Python Columbus
```

### Multiple Groups Support

The bot is designed to easily support multiple groups. You can extend it to support group-specific commands:

```python
# Future enhancement: !ask python_columbus <question>
# Future enhancement: !ask javascript_columbus <question>
```

## API Keys Setup

### Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section
4. Create a bot and copy the token
5. Add the bot to your server with appropriate permissions

### Brave Search API Key

1. Visit [Brave Search API](https://api.search.brave.com/)
2. Sign up for an account
3. Generate an API key
4. The free tier includes 10,000 queries per month

### Groq API Key

1. Go to [Groq Console](https://console.groq.com/)
2. Create an account
3. Generate an API key
4. Groq offers fast inference with various models

## Data Sources

### Meetup Events Page
- **Event Details**: Title, date, time, location, description
- **Group Information**: Member count, location, timezone, status
- **RSVP Data**: Number of attendees, event status
- **Venue Information**: Address, city, state, country
- **Creator Information**: Event organizer details

### Official Website
- **Group Description**: Mission, purpose, community information
- **Contact Information**: Social media, contact details
- **Additional Resources**: Links, documentation, community guidelines
- **About Pages**: Group history, leadership, policies

## Architecture

```
Discord Bot
    ↓
brave_search() - Fetches data from multiple sources
    ↓
fetch_meetup_data() - Scrapes Meetup events page
fetch_website_data() - Scrapes official website
    ↓
extract_comprehensive_meetup_data() - Parses JSON data
    ↓
ask_groq() - AI-powered response generation
    ↓
Discord Response
```

## Future Enhancements

### RAG (Retrieval-Augmented Generation)
- **Vector Database**: Store event embeddings for semantic search
- **Chunking**: Split large documents into searchable chunks
- **Hybrid Search**: Combine keyword and semantic search
- **Context Window**: Maintain conversation history

### MCP (Model Context Protocol)
- **Tool Integration**: Connect to calendar APIs, weather services
- **External APIs**: Integrate with Eventbrite, Facebook Events
- **Real-time Updates**: Webhook support for live event updates
- **Multi-modal**: Support for images, maps, and rich media

### Advanced Features
- **Event Reminders**: Automatic notifications for upcoming events
- **RSVP Tracking**: Monitor event attendance changes
- **Analytics**: Track popular events and engagement
- **Multi-language Support**: International group support
- **Slash Commands**: Native Discord slash command integration

## Troubleshooting

### Common Issues

1. **Bot Not Responding**
   - Check Discord token is correct
   - Verify bot has message content intent enabled
   - Ensure bot is added to the server

2. **API Errors**
   - Verify all API keys are set correctly
   - Check API rate limits
   - Ensure internet connectivity

3. **No Event Data**
   - Verify Meetup URL is correct
   - Check if group has public events
   - Review network connectivity

### Logging

The bot includes comprehensive logging. Check the console output for:
- Data fetching status
- API response details
- Error messages
- User interaction logs



## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📊 Project Status

[![GitHub stars](https://img.shields.io/github/stars/yourusername/ccc_bot?style=social)](https://github.com/yourusername/ccc_bot)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/ccc_bot?style=social)](https://github.com/yourusername/ccc_bot)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/ccc_bot)](https://github.com/yourusername/ccc_bot/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/ccc_bot)](https://github.com/yourusername/ccc_bot/pulls)


### 📈 Roadmap

- [ ] **RAG Implementation**: Vector database integration for semantic search
- [ ] **MCP Support**: Model Context Protocol for enhanced tool integration
- [ ] **Slash Commands**: Native Discord slash command support
- [ ] **Event Reminders**: Automatic notifications for upcoming events
- [ ] **Multi-language Support**: International group support
- [ ] **Analytics Dashboard**: Track popular events and engagement

### ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/ccc_bot&type=Date)](https://star-history.com/#yourusername/ccc_bot&Date)

---

**Note**: This bot is designed for educational and community use. Please respect Meetup's terms of service and rate limits when using this tool.

### 🙏 Acknowledgments

- [Discord.py](https://discordpy.readthedocs.io/) - Discord API wrapper
- [Groq](https://console.groq.com/) - Fast LLM inference
- [Brave Search](https://api.search.brave.com/) - Web search API
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Web scraping
- [Meetup](https://www.meetup.com/) - Event platform
