import gspread
from google.oauth2.service_account import Credentials
import os

def send_to_sheet(name, email, subject, message):
    creds_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        creds_file,
        scopes=scopes
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1
    sheet.append_row([name, email, subject, message])
