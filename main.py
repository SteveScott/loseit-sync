
## import libraries
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from dotenv import  load_dotenv
from pathlib import Path

## load the environment variables
load_dotenv(f"C:\\Users\\{os.getlogin()}\\secrets\.dotenv")
### connect to googe drive
gauth = GoogleAuth()
gauth.LoadClientConfigFile(f"C:\\Users\\{os.getlogin()}\\secrets\\client_secrets.json")
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

### List the files in the MyDrive/LoseIt directory
file_list = drive.ListFile({'q': "'LoseIt' in parents and trashed=false"}).GetList()
print(file_list)