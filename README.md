# AG Patch Randomizer

A simple Python UI for fetching a list of items from a Google Sheets spreadsheet, picking a random item from the list with odds based on inventory numbers, and finally updating it to the spreadsheet

## How to run

Running in virtualenv is recommended 

1. Run `pip install -r requirements.txt`

2. Run `ui.py`

# Potential issues

`invalid_grant` error occurs when running the program (should probably not occur with service account but put here in case I forget about this and encounter it again)

 - This occurs due to OAuth API credentials expiring after 7 days. 
    1. Delete `%APPDATA%\gspread\authorized_user.json` (Windows) or `~/config/gspread/authorized_user.json` (everhthing else)
    2. Delete `token.json`
    3. Run `ui.py` again. This should prompt the login screen and everything should work nicely once again 