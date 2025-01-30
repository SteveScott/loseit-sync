
## import libraries
import os
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import  load_dotenv
from pathlib import Path
import logging
## load the environment variables
logging.basicConfig(level=logging.INFO)
load_dotenv(f"C:\\Users\\{os.getlogin()}\\secrets\\.dotenv")

### connect to googe drive
flow = InstalledAppFlow.from_client_secrets_file(
    f"""c:\\users\\{os.getlogin()}\\secrets\\client_secrets.json""",
    scopes= [
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email',
            'openid'
    ]
)
flow.run_local_server()
credentials = flow.credentials

## create an oauth2 service object to test drive.

user_info_service = build('oauth2', 'v2', credentials=credentials)
user_info = user_info_service.userinfo().get().execute()
print(f"logged in as {user_info['email']}")


#connect to google drive.
#loseit files can be anywhere in the drive under the folder name LoseIt
folder_name = "LoseIt"
service = build('drive', 'v3', credentials=credentials)
logging.info('service is created')

#find the LoseIt folder
query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and 'root' in parents"
results : Resource = service.files().list(
    q=query,
    spaces='drive',
    fields='files(id,name)'
).execute()

items = results.get('files', [])
if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(f"{item['name']} ({item['id']})")

# If the folder is found, use its ID to list files within it
if items:
    folder_id = items[0]['id']
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)'
    ).execute()

    items = results.get('files', [])
    if not items:
        print('No files found in LoseIt folder.')
    else:
        print('Files in LoseIt folder:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

logging.info(f"the results are {results}")
service.close()
logging.info('service is closed')
