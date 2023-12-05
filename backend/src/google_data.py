import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/drive"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
SAMPLE_SPREADSHEET_ID_2 = "1b9E8FIy3cgeNqitfEaY-Li0ygXDFpJo0dwjVUxZu5lM"
SAMPLE_RANGE_NAME = "Class Data!A2:E"
SAMPLE_DRIVE_ID = "1pp56tRq-gdel-eNoILS5MZEIj3G4cLTC" # "1BekPg1GP-HX6LFoibDeYsbb_gibSNuyB"

sheets_service = None
drive_service = None
creds = None

logging = False

CWD = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = CWD + "/../config/token.json"
CREDENTIALS_PATH = CWD + "../config/credentials.json"

def log(txt):
    if(logging):
        print(txt)

# Obtain OAuth2.0 credentials (or credentials obtained from previous run if
# still available)
def get_creds():
    global creds

    if creds:
        return creds
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds

# Get the sheets service if it hasn't already been built
def get_sheets_service(creds):
    global sheets_service
    if sheets_service == None:
        sheets_service = build("sheets", "v4", credentials=creds)
    return sheets_service

# Get the drive service if it hasn't already been built
def get_drive_service(creds):
    global drive_service
    if drive_service == None:
        drive_service = build("drive", "v3", credentials=creds)
    return drive_service

# Get the values of the spreadsheet w/ spreadsheet_id in the given range
def get_spreadsheet_range(spreadsheet_id, range):
    creds = get_creds()
    vals = None

    try:
        service = get_sheets_service(creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
                .get(spreadsheetId=spreadsheet_id, range=range)
                .execute()
        )
        values = result.get("values", [])
        vals = values

        if not values:
            log("No data found.")
            return

        log("Name:")
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            # log(f"{row[0]}")
            pass
    except HttpError as err:
        log(err)
    
    return vals

def clear_spreadsheet_range(spreadsheet_id, range):
    creds = get_creds()

    try:
        service = get_sheets_service(creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .clear(
                spreadsheetId=spreadsheet_id,
                range=range,
            )
            .execute()
        )

        log(f"{result.get('clearedRange')} cells cleared.")
        return result
    except HttpError as error:
        log(f"An error occurred: {error}")
        return error

# Updates a range of values in a given spreadsheet
def update_spreadsheet_range(spreadsheet_id, range_name, values):
    creds = get_creds()

    try:
        service = get_sheets_service(creds)
        body = {
            "values": values
        }
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                body=body,
                valueInputOption="USER_ENTERED"
            )
            .execute()
        )
        log(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        log(f"An error occurred: {error}")
        return error


# Get information about all the files in the folder with ID of drive_id
def get_files_in_folder(drive_id):
    creds = get_creds()
    files = []

    try:
        service = get_drive_service(creds)

        # Call the Drive v3 API
        results = (
            service.files()
            .list(
                q=f"'{drive_id}' in parents and trashed=false")
            .execute()
        )

        log(results)
        items = results.get("files", [])

        if not items:
            log("No files found.")
            return
        log("Files:")
        for item in items:
            log(f"{item['name']} ({item['id']})")
            files.append(item)
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        log(f"An error occurred: {error}")
    
    return files

if __name__ == "__main__":
    logging = True
    get_spreadsheet_range(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
    get_files_in_folder(SAMPLE_DRIVE_ID)
    update_spreadsheet_range(SAMPLE_SPREADSHEET_ID_2, "B13:B15", [["He"], ["lo"], ["world"]])