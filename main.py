
## import libraries
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import  load_dotenv
from pathlib import Path
import logging
## load the environment variables
load_dotenv(f"C:\\Users\\{os.getlogin()}\\secrets\.dotenv")
### connect to googe drive

flow = InstalledAppFlow.from_client_secrets_file(
    f"""c:\\users\\{os.getlogin()}\\secrets\\client_secrets.json""",
    scopes= "https://www.googleapis.com/auth/userinfo.profile openid https://www.googleapis.com/auth/userinfo.email"
)
flow.run_local_server()
credentials = flow.credentials
'''
auth_uri = flow.authorization_url()
code = input("Enter the authorization code")
flow.fetch_token(code=code)
'''
service = build('drive', 'v3', credentials=credentials)
user_info_service = build('oauth2', 'v2', credentials=credentials)
user_info = user_info_service.userinfo().get().execute()
print(user_info['email'])
service.close()
logging.info('service is closed')
