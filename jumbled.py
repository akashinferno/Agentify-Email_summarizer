# JUMBLED FUNCTIONS FOR AGENT BUILDING COMPETITION
# Functions are provided in random order with code block numbers
# Participants need to analyze empty_main.py and use these functions correctly

import os
import base64
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from google import genai

load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# ========== CODE BLOCK 1 ==========
def display_results(summary):
    """
    Displays the final email summary in a formatted way
    Args: summary (str) - The AI-generated summary to display
    """
    separator = "=" * 30
    print(f"\n{separator}")
    print("📩 EMAIL SUMMARY REPORT 📩")
    print(separator)
    print(f"\n{summary}")
    print(f"\n{separator}\n")

# ========== CODE BLOCK 2 ==========
def get_emails(service, days=5):
    """
    Fetches recent emails from Gmail account
    Args: service - Gmail API service object
          days (int) - Number of days back to fetch emails (default: 5)
    Returns: str - Combined email content (subjects and snippets)
    """
    # Calculate the date range
    current_time = datetime.datetime.utcnow()
    past_date = current_time - datetime.timedelta(days=days)
    search_date = past_date.strftime('%Y/%m/%d')
    
    # Build search query
    search_query = f'after:{search_date}'
    
    # Get message list
    response = service.users().messages().list(userId='me', q=search_query).execute()
    message_list = response.get('messages', [])
    
    # Process emails
    email_content = []
    for message in message_list[:5]:  # Process first 5 emails
        full_message = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        message_payload = full_message['payload']
        message_headers = message_payload.get('headers', [])
        
        # Extract subject
        email_subject = 'No Subject'
        for header in message_headers:
            if header['name'] == 'Subject':
                email_subject = header['value']
                break
        
        # Get snippet
        email_snippet = full_message.get('snippet')
        
        # Format email entry
        email_entry = f"Subject: {email_subject}\nSnippet: {email_snippet}\n---"
        email_content.append(email_entry)
    
    return "\n\n".join(email_content)

# ========== CODE BLOCK 3 ==========
def get_gmail_service():
    """
    Authenticates and creates Gmail API service object
    Handles OAuth2 flow and token management
    Returns: Gmail service object for API calls
    """
    credentials = None
    token_file = 'token.json'
    
    # Load existing credentials if available
    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # Refresh or create new credentials
    if not credentials or not credentials.valid:
        oauth_flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        credentials = oauth_flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open(token_file, 'w') as token_writer:
            token_writer.write(credentials.to_json())
    
    # Build and return Gmail service
    gmail_service = build('gmail', 'v1', credentials=credentials)
    return gmail_service

# ========== CODE BLOCK 4 ==========
def summarize_text(text):
    """
    Uses Google Gemini AI to summarize email content
    Args: text (str) - Combined email content to summarize
    Returns: str - AI-generated summary with bullet points
    """
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Initialize Gemini client
    gemini_client = genai.Client(api_key=api_key)
    
    # Create prompt for summarization
    prompt = f"Summarize the following emails into a concise, line-by-line bulleted list. Each summary point should start with a bullet point (*).\n\n{text}"
    
    # Generate summary using Gemini
    ai_response = gemini_client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    
    # Extract and return summary text
    email_summary = ai_response.text
    return email_summary
