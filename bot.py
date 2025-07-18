import os
import discord
import requests
from dotenv import load_dotenv
import openai  # used for Groq-compatible LLMs if wrapped
import logging
from bs4 import BeautifulSoup
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check for required environment variables
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is required")
if not BRAVE_API_KEY:
    raise ValueError("BRAVE_API_KEY environment variable is required")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required")

# Global configuration for different event groups
EVENT_GROUPS = {
    "columbus_code_coffee": {
        "name": "Columbus Code & Coffee",
        "meetup_url": ("https://www.meetup.com/columbus-code-and-coffee/"
                      "events/"),
        "website_url": "https://cbuscodeandcoffee.com/",
        "description": ("Software engineering community for developers by "
                       "developers")
    },
    # Add more groups here easily
    # "another_group": {
    #     "name": "Another Meetup Group",
    #     "meetup_url": "https://www.meetup.com/another-group/events/",
    #     "website_url": "https://another-group.com/",
    #     "description": "Description of the group"
    # }
}

# Default group to use
DEFAULT_GROUP = "columbus_code_coffee"

# Use intents that include message content
intents = discord.Intents.default()
intents.message_content = True  # This is needed to read message content

client = discord.Client(intents=intents)


def brave_search(query, group_key=DEFAULT_GROUP):
    """Fetch comprehensive information from multiple sources for a specific group"""
    if group_key not in EVENT_GROUPS:
        logger.error(f"Unknown group key: {group_key}")
        return (f"Error: Unknown group '{group_key}'. "
                f"Available groups: {list(EVENT_GROUPS.keys())}")
    
    group_config = EVENT_GROUPS[group_key]
    logger.info(f"Fetching comprehensive information for "
               f"{group_config['name']}")
    
    # Get Meetup event data
    meetup_data = fetch_meetup_data(group_config)
    
    # Get official website data
    website_data = fetch_website_data(group_config)
    
    # Combine all information
    combined_data = f"""
{meetup_data}

{website_data}
"""
    
    logger.info(f"Combined data length: {len(combined_data)} characters")
    # Only log first 500 chars to avoid sensitive data
    safe_preview = combined_data[:500].replace('\n', ' ').replace('\r', ' ')
    logger.info(f"Combined data preview: {safe_preview}...")
    
    return combined_data


def fetch_meetup_data(group_config):
    """Fetch event and group data from Meetup for a specific group"""
    meetup_url = group_config["meetup_url"]
    
    logger.info(f"Fetching Meetup data from: {meetup_url}")
    
    try:
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36'),
            'Accept': ('text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,*/*;q=0.8'),
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(meetup_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the __NEXT_DATA__ script tag
        next_data_script = soup.find('script', id='__NEXT_DATA__')
        
        if next_data_script:
            logger.info("Found __NEXT_DATA__ script tag")
            
            try:
                json_data = json.loads(next_data_script.get_text())
                logger.info("Successfully parsed Meetup JSON data")
                return extract_comprehensive_meetup_data(json_data, group_config)
                    
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing Meetup JSON: {e}")
        
        logger.info("No Meetup JSON data found, using fallback")
        return extract_div_content_fallback(soup)
        
    except Exception as e:
        logger.error(f"Error fetching Meetup data: {e}")
        return "Error fetching Meetup data"


def fetch_website_data(group_config):
    """Fetch comprehensive information from the official website"""
    website_url = group_config["website_url"]
    
    logger.info(f"Fetching website data from: {website_url}")
    
    try:
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36'),
            'Accept': ('text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,*/*;q=0.8'),
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(website_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for element in soup(["script", "style"]):
            element.decompose()
        
        # Extract all text content
        page_text = soup.get_text(separator=' ', strip=True)
        
        # Clean up the text
        lines = [line.strip() for line in page_text.splitlines() 
                if line.strip()]
        clean_text = ' '.join(lines)
        
        logger.info(f"Website data length: {len(clean_text)} characters")
        
        return f"""
OFFICIAL WEBSITE INFORMATION:
{clean_text}
"""
        
    except Exception as e:
        logger.error(f"Error fetching website data: {e}")
        return "Error fetching website data"


def extract_comprehensive_meetup_data(json_data, group_config):
    """Extract comprehensive event and group information from Meetup JSON"""
    try:
        apollo_state = (json_data.get('props', {})
                       .get('pageProps', {})
                       .get('__APOLLO_STATE__', {}))
        
        meetup_info = []
        
        # Extract group information
        group_info = ""
        for key, value in apollo_state.items():
            if key.startswith('Group:'):
                group_data = value
                stats = group_data.get('stats', {})
                event_ratings = stats.get('eventRatings', {})
                
                group_info = f"""
MEETUP GROUP INFORMATION:
Name: {group_data.get('name', 'Unknown Group')}
Members: {stats.get('memberCounts', {}).get('all', 0)}
Location: {group_data.get('city', '')}, {group_data.get('state', '')}
Country: {group_data.get('country', 'Unknown')}
Timezone: {group_data.get('timezone', 'Unknown')}
Join Mode: {group_data.get('joinMode', 'Unknown')}
Status: {group_data.get('status', 'Unknown')}
Welcome Message: {group_data.get('welcomeBlurb', 'No welcome message')}
Average Event Rating: {event_ratings.get('average', 'N/A')}
Total Event Ratings: {event_ratings.get('total', 'N/A')}
"""
                break
        
        meetup_info.append(group_info)
        
        # Extract all events (upcoming, past, etc.)
        events_info = []
        for key, value in apollo_state.items():
            if key.startswith('Event:'):
                event_data = value
                
                # Extract comprehensive event details
                event_info = {
                    'title': event_data.get('title', 'Unknown Event'),
                    'dateTime': event_data.get('dateTime', 'No date'),
                    'endTime': event_data.get('endTime', 'No end time'),
                    'description': event_data.get('description', 'No description'),
                    'eventUrl': event_data.get('eventUrl', 'No URL'),
                    'status': event_data.get('status', 'Unknown status'),
                    'going_count': (event_data.get('going', {})
                                   .get('totalCount', 0)),
                    'rsvpState': event_data.get('rsvpState', 'Unknown'),
                    'eventType': event_data.get('eventType', 'Unknown'),
                    'isOnline': event_data.get('isOnline', False),
                    'createdTime': event_data.get('createdTime', 'Unknown')
                }
                
                # Get venue information if available
                venue_ref = event_data.get('venue', {}).get('__ref', '')
                if venue_ref and venue_ref in apollo_state:
                    venue_data = apollo_state[venue_ref]
                    event_info['venue'] = {
                        'name': venue_data.get('name', 'Unknown venue'),
                        'address': venue_data.get('address', 'No address'),
                        'city': venue_data.get('city', ''),
                        'state': venue_data.get('state', ''),
                        'country': venue_data.get('country', '')
                    }
                
                # Get creator information
                creator_ref = (event_data.get('creatorMember', {})
                              .get('__ref', ''))
                if creator_ref and creator_ref in apollo_state:
                    creator_data = apollo_state[creator_ref]
                    event_info['creator'] = creator_data.get('name', 'Unknown')
                
                # Format the event information
                formatted_event = f"""
EVENT: {event_info['title']}
Date: {event_info['dateTime']}
End Time: {event_info['endTime']}
Status: {event_info['status']}
Event Type: {event_info['eventType']}
Is Online: {event_info['isOnline']}
RSVP State: {event_info['rsvpState']}
Going: {event_info['going_count']} people
Created: {event_info['createdTime']}
Creator: {event_info.get('creator', 'Unknown')}
URL: {event_info['eventUrl']}
"""
                
                if 'venue' in event_info:
                    venue = event_info['venue']
                    formatted_event += f"""Venue: {venue['name']}
Address: {venue['address']}, {venue['city']}, {venue['state']}, {venue['country']}
"""
                
                formatted_event += f"""
Description: {event_info['description']}
"""
                
                events_info.append(formatted_event)
        
        # Sort events by date (upcoming first)
        def get_date_key(event_str):
            try:
                date_line = [line for line in event_str.split('\n') 
                           if line.startswith('Date: ')][0]
                return date_line.replace('Date: ', '')
            except Exception:
                return '9999'
        
        events_info.sort(key=get_date_key)
        
        # Add events to meetup info
        if events_info:
            meetup_info.append("MEETUP EVENTS:")
            meetup_info.extend(events_info)
        else:
            meetup_info.append("No events found in Meetup data")
        
        # Extract member information (limit to avoid sensitive data)
        members_info = []
        for key, value in apollo_state.items():
            if key.startswith('Member:'):
                member_data = value
                member_info = f"Member: {member_data.get('name', 'Unknown')}"
                members_info.append(member_info)
        
        if members_info:
            meetup_info.append(f"\nRECENT MEMBERS ({len(members_info)} found):")
            meetup_info.extend(members_info[:10])  # Show first 10 members
        
        return "\n".join(meetup_info)
            
    except Exception as e:
        logger.error(f"Error extracting comprehensive Meetup data: {e}")
        return f"Error extracting Meetup data: {str(e)}"


def extract_div_content_fallback(soup):
    """Fallback method to extract content from divs if JSON parsing fails"""
    # Function to recursively extract content from all divs
    def extract_div_content(element, depth=0):
        content_parts = []
        
        # Get direct text content from this element
        direct_text = element.get_text(separator=' ', strip=True)
        if direct_text and len(direct_text) > 5:
            indent = "  " * depth
            content_parts.append(f"{indent}Level {depth}: {direct_text}")
            # Limit logged content to avoid sensitive data
            safe_text = direct_text[:200].replace('\n', ' ').replace('\r', ' ')
            logger.info(f"{indent}Level {depth} content: {safe_text}...")
        
        # Recursively process all child divs
        for child_div in element.find_all('div', recursive=False):
            child_content = extract_div_content(child_div, depth + 1)
            content_parts.extend(child_content)
        
        return content_parts
    
    # Start from the body element to get all nested divs
    body = soup.find('body')
    if body:
        all_div_content = extract_div_content(body)
    else:
        # Fallback to root if no body found
        all_div_content = extract_div_content(soup)
    
    logger.info(f"Extracted content from {len(all_div_content)} div levels")
    
    # Combine all content
    combined_content = '\n\n'.join(all_div_content)
    
    logger.info(f"Combined nested div content length: {len(combined_content)} chars")
    # Only log first 500 chars to avoid sensitive data
    safe_preview = combined_content[:500].replace('\n', ' ').replace('\r', ' ')
    logger.info(f"Combined content preview: {safe_preview}...")
    
    return combined_content


def brave_search_fallback(query):
    """Fallback method using Brave search API"""
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    
    # Simple search for the events page
    search_queries = [
        f'site:meetup.com/columbus-code-and-coffee/events "{query}"',
        f'"{query}" "Columbus Code and Coffee" site:meetup.com'
    ]
    
    all_results = []
    
    for search_query in search_queries:
        params = {
            "q": search_query,
            "count": 5
        }
        
        logger.info(f"Brave search fallback for: {search_query}")
        try:
            resp = requests.get(url, headers=headers, params=params).json()
            results = resp.get("web", {}).get("results", [])
            all_results.extend(results)
            logger.info(f"Found {len(results)} results for this query")
        except Exception as e:
            logger.error(f"Error in Brave search: {e}")
    
    # Remove duplicates
    seen_urls = set()
    unique_results = []
    for result in all_results:
        url = result.get("url", "")
        if url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)
    
    snippets = []
    for i, item in enumerate(unique_results):
        title = item.get("title", "No title")
        description = item.get("description", "No description")
        url = item.get("url", "No URL")
        
        logger.info(f"Result {i+1}:")
        logger.info(f"  Title: {title}")
        logger.info(f"  URL: {url}")
        # Limit description logging to avoid sensitive data
        safe_desc = description[:200].replace('\n', ' ').replace('\r', ' ')
        logger.info(f"  Description: {safe_desc}")
        
        snippets.append(description)
    
    combined_snippets = "\n".join(snippets)
    logger.info(f"Combined snippets length: {len(combined_snippets)} chars")
    
    return combined_snippets


def ask_groq(question, context):
    prompt = f"""You are a helpful assistant for Columbus Code and Coffee events. 
Use ONLY the information provided below to answer the question.

Information from the Meetup events page:
{context}

Question: {question}

Instructions:
- Carefully analyze the provided content for any event information
- Look for dates, times, locations, and event descriptions
- If you find event details, present them clearly and completely
- If the content seems incomplete or doesn't contain current events, 
  explain what you found and suggest checking the official Meetup page
- Be specific about what information is available vs. what's missing
- If you see navigation elements or page structure instead of events, 
  acknowledge this and provide helpful guidance
- Always be helpful and informative, even if the content is limited

Answer:"""

    # Use the updated OpenAI API format
    client = openai.OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # replace with correct Groq model
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("Bot is ready! Commands available:")
    print("- !ask <question>")
    print("- /ask <question>")
    print(f"Tracking events for: {EVENT_GROUPS[DEFAULT_GROUP]['name']}")
    print(f"Available groups: {list(EVENT_GROUPS.keys())}")


@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Log all messages for debugging (but sanitize content)
    safe_content = message.content.replace('\n', ' ').replace('\r', ' ')
    logger.info(f"Received message: '{safe_content}' from {message.author}")
    
    # Check for !ask command
    if message.content.startswith("!ask "):
        query = message.content[len("!ask "):]
        logger.info(f"Processing !ask command: {query}")
        try:
            context = brave_search(query)
            answer = ask_groq(query, context)
            await message.channel.send(answer)
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            logger.error(f"Error processing !ask command: {e}")
            await message.channel.send(error_msg)
    
    # Check for /ask command (slash command)
    elif message.content.startswith("/ask "):
        query = message.content[len("/ask "):]
        logger.info(f"Processing /ask command: {query}")
        try:
            context = brave_search(query)
            answer = ask_groq(query, context)
            await message.channel.send(answer)
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            logger.error(f"Error processing /ask command: {e}")
            await message.channel.send(error_msg)
    
    # Check for just "!ask" or "/ask" without a question
    elif message.content in ["!ask", "/ask"]:
        usage_msg = ("Please provide a question! Usage: `!ask <your question>` "
                    "or `/ask <your question>`")
        await message.channel.send(usage_msg)
    
    # Log if message doesn't match any command
    else:
        logger.info(f"Message doesn't match any command pattern: {safe_content}")


client.run(DISCORD_TOKEN)
