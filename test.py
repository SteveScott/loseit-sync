import pytest
from gdrive import GDrive

## import libraries
import os
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from dotenv import  load_dotenv
from google.oauth2.credentials import Credentials
from pathlib import Path
import logging
## load the environment variables
logging.basicConfig(level=logging.INFO)

load_dotenv(f'c:\\users\\{os.getlogin()}\\secrets\\.env')

@pytest.fixture(scope='module')
def gdrive():
    return GDrive()

def test_passing():
    assert (1, 2, 3) == (1, 2, 3)

#def test_failing():
#    assert (1, 2, 3) == (3, 2, 1)

def test_google(gdrive : GDrive):
    #tests the connection to google drive by printing the user's email address it received from Google API.
    service : Resource = gdrive.connect_to_service('oauth2', gdrive.credentials, 'v2')
    user_info = service.userinfo().get().execute()
    print(f"logged in as {user_info['email']}") 
    assert user_info['email'] == os.getenv('GOOGLE_EMAIL')

def test_gdrive(gdrive):
    #connect to google drive.
    service = gdrive.connect_to_service('drive', gdrive.credentials, 'v3')
    assert service is not None
    page_token=None
    results = service.files().list(q="'root' in parents and mimeType = 'application/vnd.google-apps.folder'",
                                   spaces='drive', 
                                   fields='nextPageToken, files(id, name)', 
                                   pageToken=page_token,
                                   ).execute()
    items = results.get('files', [])
    if not items:
        raise AssertionError(f'No files found in test_gdrive. Results is {results}')
    else:
        assert items[0]['id'] is not None

def test_find_loseit_folder(gdrive):
    #find the folder id of the loseit folder
    folder_id = gdrive.find_loseit_folder()
    assert folder_id is not None, "no files found in test_find_loseit_folder. Expecting a folder id"

