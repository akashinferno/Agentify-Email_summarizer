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
    print("\n===== 📩 Email Summary =====\n")
    print(summary)
    print("\n============================")

# ========== CODE BLOCK 2 ==========
def get_emails(service, days=5):
    """
    Fetches recent emails from Gmail account
    Args: service - Gmail API service object
          days (int) - Number of days back to fetch emails (default: 5)
    Returns: str - Combined email content (subjects and snippets)
    """
    date_from = (datetime.datetime.utcnow() - datetime.timedelta(days=days)).strftime('%Y/%m/%d')
    query = f'after:{date_from}'

    result = service.users().messages().list(userId='me', q=query).execute()
    messages = result.get('messages', [])

    emails = []
    for msg in messages[:5]:  # limit to last 5 emails for speed
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data['payload']
        headers = payload.get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        snippet = msg_data.get('snippet')
        emails.append(f"Subject: {subject}\nSnippet: {snippet}\n---")
    return "\n\n".join(emails)

# ========== CODE BLOCK 3 ==========
def get_gmail_service():
    """
    Authenticates and creates Gmail API service object
    Handles OAuth2 flow and token management
    Returns: Gmail service object for API calls
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

# ========== CODE BLOCK 4 ==========
def summarize_text(text):
    """
    Uses Google Gemini AI to summarize email content
    Args: text (str) - Combined email content to summarize
    Returns: str - AI-generated summary with bullet points
    """
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"Summarize the following emails into a concise, line-by-line bulleted list. Each summary point should start with a bullet point (*).\n\n{text}"
    )
    
    summary = response.text
    return summary
