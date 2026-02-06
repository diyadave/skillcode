import gspread
import os
import json
from google.oauth2.service_account import Credentials

def send_to_sheet(name, email, subject, message):
    creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not creds_json:
        raise Exception("GOOGLE_SERVICE_ACCOUNT_JSON not set")

    creds_info = json.loads(creds_json)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        creds_info,
        scopes=scopes
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1
    sheet.append_row([name, email, subject, message])
