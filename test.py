import pytest
from gdrive import GDrive
import platform
from time import sleep
from loseit import LoseIt
import platform

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

@pytest.fixture(scope='module')
def loseit():
    return LoseIt()

def test_passing():
    assert (1, 2, 3) == (1, 2, 3)

#def test_failing():
#    assert (1, 2, 3) == (3, 2, 1)

def test_google(gdrive : GDrive):
    #tests the connection to google drive by printing the user's email address it received from Google API.
    service : Resource = gdrive.connect_to_service('oauth2', gdrive.credentials, 'v2')
    user_info = service.userinfo().get().execute()
    print(f"logged in as {user_info['email']}") 
    test_email_address = os.getenv('GOOGLE_EMAIL')
    assert test_email_address is not None
    assert user_info['email'] == test_email_address

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

def test_lose_it_download(loseit : LoseIt):
    try:
        loseit.loseit_download()
    except NotImplementedError:
        assert True
def test_remove_loseit_files(loseit : LoseIt):
    #side effect: will remove the loset-export folder
    download_path = loseit.get_download_path()
    loseit.remove_loseit_files()
    extract_dir = os.path.join(download_path, "loseit-export")
    assert not os.path.exists(extract_dir)

def test_extract_loseit_files(loseit : LoseIt):
    #side effect: will re-create the loseit-export folder
    download_path= loseit.get_download_path()
    extract_dir = os.path.join(download_path, "loseit-export")
    loseit.extract_losit_files()
    assert os.path.exists(extract_dir)
    

