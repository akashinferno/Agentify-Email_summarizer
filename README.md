# 📩 Gmail Summarize Agent

A Python application that connects to your Gmail account, retrieves emails, and summarizes their content using AI. This project is ideal for users who want to quickly understand the gist of their inbox without reading every email in detail.

---

## ✨ Features
- Authenticate with Gmail using OAuth2  
- Fetch recent emails from your inbox  
- Summarize email content using AI (Gemini)  
- Simple command-line interface  

---

## 🛠 Prerequisites
- Python 3.7+  
- Gmail account  
- Google Cloud project with Gmail API enabled  

---

## ⚙️ Setup

bash
# 1. Clone the Repository
git clone <repo-url>
cd Gmail_summarize_agent

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Setup Gmail API
 - Go to Google Cloud Console: https://console.cloud.google.com/
 - Create a new project
 - Open APIs & Services → Library
 - Search for Gmail API and click Enable
 - Go back to APIs & Services → Credentials
 - Click + Create Credentials → OAuth client ID
 - Configure the Consent Screen:
     * Enter App name and Email
     * Choose External
     * Add a contact email
     * Scroll down to Test Users, click Add Users, and enter allowed Gmail addresses (at least your own)
     * Save changes
     * Agree to terms and click Finish
 - Create the OAuth client:
     * Select Application type → Desktop app
     * Enter a name and click Create
 - Download the JSON file
 - Rename the file to credentials.json
 - Move it into your project folder

# 4. Setup Gemini API
 - Go to Google AI Studio: https://aistudio.google.com/
 - Click Get API Key
 - Click + Create API Key
 - Select your Google Cloud project from the dropdown
 - Copy the API key
 - In your project folder, create a file named .env
 - Add the following line inside .env:
     GEMINI_API_KEY={paste your API key here}

# 5. Run the Application
python app.py

   

## Usage
- On first run, you will be prompted to authenticate with your Google account.
- The app will fetch recent emails and display their summaries.

## File Structure
- `app.py` — Main application logic
- `requirements.txt` — Python dependencies
- `credentials.json` — Google API credentials (not included)
- `token.json` — OAuth2 token (generated after first run)
