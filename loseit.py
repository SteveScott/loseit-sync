import os
import platform
import requests
import logging
import shutil
from time import sleep
import zipfile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by   import By
from dotenv import load_dotenv

class LoseIt :
    '''
    the class that downloads and exracts loseit files.
    '''
    def __init__(self):
        load_dotenv(f'c:\\users\\{os.getlogin()}\\secrets\\.env')
        self.LOSEIT_USERNAME = os.getenv("LOSEIT_USERNAME")
        self.LOSEIT_PASSWORD = os.getenv("LOSEIT_PASSWORD")
        self.LOSEIT_LOGIN_URL="https://my.loseit.com/login?r=https%3A%2F%2Fwww.loseit.com%2Fexport%2Fdata%3Fnull"
        self.LOSEIT_DOWNLOAD_URL="http://loseit.com/export/data"
        system_type = platform.system()
        self.FILENAME = "loseit-export.zip"
        self.download_path = self.get_download_path()

    def loseit_download(self): 
        raise NotImplementedError("loseit seems to be blocking download attempts.")   
        driver = webdriver.Edge()

        driver.get(self.LOSEIT_LOGIN_URL)
        username_field = driver.find_element(By.ID, 'email')
        password_field = driver.find_element(By.ID, 'password')
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        username_field.send_keys(self.LOSEIT_USERNAME)
        password_field.send_keys(self.LOSEIT_PASSWORD)
        sleep(1)
        #submit_button.click()
        driver.execute_script("alert('Try pressing the button manually and see if it downloads you have five seconds')")
        sleep(5)

        driver.get(self.LOSEIT_DOWNLOAD_URL)
        file_name = "loseit-export.zip"
        file_path = os.path.join(self.download_path, file_name )

        while not os.path.exists(file_path):
            sleep(1)

        logging.info(f"file downloaded to {file_path}")
    
    def extract_losit_files(self):
        zip_path = os.path.join(self.download_path, 'loseit-export.zip')
        extract_dir = os.path.join(self.download_path, 'loseit-export')
        
        if os.path.exists(zip_path):
            self.remove_loseit_files()
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            logging.info(f"Extracted files to {extract_dir}")
        else:
            raise FileNotFoundError(f'there is no zip file at {zip_path}')

    def remove_loseit_files(self):
        filepath = os.path.join(self.download_path, 'loseit-export')
        if os.path.exists(filepath):
            shutil.rmtree(filepath)
            logging.info(f"Removed directory and all its contents: {filepath}")
        else:
            logging.info(f"Directory does not exist: {filepath}")

    def get_download_path(self) -> str:
        system_type = platform.system()
        if system_type == 'Windows':
            return f"C:\\Users\\{os.getlogin()}\\Downloads\\"
        else:
            return f"/home/{os.getlogin()}/Downloads/"