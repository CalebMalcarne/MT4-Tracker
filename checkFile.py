import os
from edit_config import *

def makeFiles():
    cfgfile = '''
{
    "mt4_files_directory": "Directory",
    "report_time": "00:30",
    "update_delay": "1",
    "account": "account",
    "emails": "email"
}
            '''

    # Check if config.cfg exists
    if not os.path.exists("config.cfg"):
        with open("config.cfg", "w") as f:
            f.write(cfgfile)
        print("Config file created successfully.")

    # Create Sheets directory if it doesn't exist
    if not os.path.exists("Sheets"):
        os.makedirs("Sheets")
        print("Sheets directory created successfully.")

    # Create Img directory if it doesn't exist
    if not os.path.exists("Img"):
        os.makedirs("Img")
        print("Img directory created successfully.")

