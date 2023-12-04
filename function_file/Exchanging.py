from google.oauth2.service_account import Credentials
import gspread

scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file(
    "function_file/palm-2-405006-cb71860f13d0.json",
    scopes=scopes
)

gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_key('1TVwWMSxZtOgqvjIdzWvAMs_JSy8KDYt5lyA_bT0DOcw')

def exchange(currency,currency2):
  spreadsheet.sheet1.update_acell("A1",f"=GOOGLEFINANCE(\"CURRENCY:{currency}{currency2}\")")
  return spreadsheet.sheet1.acell("A1").value
