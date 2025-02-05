
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
class GDrive :
    '''
    the module that connects to google services for uploading the Loseit information.
    '''
    def __init__(self, folder_name : str = 'LoseIt'):
        load_dotenv(f"C:\\Users\\{os.getlogin()}\\secrets\\.dotenv")
        self.folder_name = folder_name
        self.credentials = self.connect_google()
        self.service = None

    def __on_exit__(self):
        if self.service:
            self.service.close()
            logging.info('service is closed')

    ### connect to googe drive
    def connect_google(self) -> Credentials:
        flow : Flow = InstalledAppFlow.from_client_secrets_file(
            f"""c:\\users\\{os.getlogin()}\\secrets\\client_secrets.json""",
            scopes= [
                    'https://www.googleapis.com/auth/drive.file',
                    'https://www.googleapis.com/auth/userinfo.profile',
                    'https://www.googleapis.com/auth/userinfo.email',
                    'https://www.googleapis.com/auth/drive.metadata.readonly',
                    'openid'
            ]
        )
        flow.run_local_server()
        credentials : Credentials = flow.credentials
        return credentials
        ## create an oauth2 service object to test drive.

    def connect_to_service(self, service: str, credentials: InstalledAppFlow, version) -> Resource:
        '''
        connects to the specified service. For google drive, the service is 'drive'
        returns Resource object. 
        The email API is currently v2
        The Drive api is currently v3
        '''
        service : Resource = build(service, version, credentials=credentials)
        return service
    
    
    
    
    #loseit files can be anywhere in the drive under the folder name LoseIt
    
    def find_loseit_folder(self) -> str:
        '''
        returns the folder id of the loseit folder
        '''
        service : Resource = self.connect_to_service('drive', self.credentials, 'v3')
        #find the LoseIt folder
        query = f"name='{self.folder_name}' and mimeType='application/vnd.google-apps.folder' and 'root' in parents"
        results : Resource = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
    
        #get the id of the LoseIT folder from the query results
        items = results.get('files', [])
        if not items:
            raise FileNotFoundError('No LoseIt folder found in Google Drive')
        else:
            print('Files:')
            for item in items:
                print(f"{item['name']} ({item['id']})")
        return items[0]['id']
    
    def list_files_in_folder(self, folder_id: str):
        '''
        lists the files in the folder
        '''
        service : Resource = self.connect_to_service('drive', self.credentials, 'v3')
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        items = results.get('files', [])
        # If the folder is found, use its ID to list files within it
        
        if not items:
            print('No files found in LoseIt folder.')
        else:
            print('Files in LoseIt folder:')
            for item in items:
                print(f"{item['name']} ({item['id']})")
    
        logging.info(f"the results are {results}")