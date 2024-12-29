import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import gspread

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
with open("sheet_id.txt") as file:
  SAMPLE_SPREADSHEET_ID = file.read()


def get_initial_list():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  range_name = "Patches!A2:A"

  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name)
        .execute()
    )
    values = result.get("values", [])
    if not values:
      print("No data found.")
      return
    flattened = [item for row in values for item in row]
    return flattened
  
  except HttpError as err:
    print(err)


def get_patches():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  range_name = "Patches!A2:B"
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name)
        .execute()
    )
    values = result.get("values", [])
    if not values:
      print("No data found.")
      return

    patches = {}
    total = 0
    for row in values:
      # Print columns A and B, which correspond to indices 0 and 1.
      inventory = int(row[1])
      total += inventory
      if (inventory != 0):
        patches[row[0]] = inventory
    #for patch in patches:
    #  prob = patches[patch]/total
    #  patches[patch] = prob
    #  print(f"{patch}, probability: {patches[patch]}")
    return patches

  except HttpError as err:
    print(err)


def update_inventory(patch):
  gc = gspread.oauth(
    credentials_filename='credentials.json',
  )
  sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
  worksheet = sh.get_worksheet(0)
  cell = worksheet.find(patch)
  print("Found something at R%sC%s" % (cell.row, cell.col))
  inventory_row = cell.row
  inventory_col = cell.col + 1
  print(f"Inventory: row {inventory_row}, col {inventory_col}") 
  val = int(worksheet.cell(inventory_row, inventory_col).value)
  print(f"Count {val}")
  updated = val - 1
  print(f"New val: {updated}")
  worksheet.update_cell(inventory_row, inventory_col, updated)