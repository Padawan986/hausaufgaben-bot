import gspread

# Authentifizierung mit Service Account
gc = gspread.service_account(filename='credentials.json')

# Öffnen des Sheets über die URL
spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1CPklXIuicJzJ8me1D1AMA64QFrCFc7m7nFJqow68yBU/edit?usp=sharing')
worksheet = spreadsheet.sheet1
