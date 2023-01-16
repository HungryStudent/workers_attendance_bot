import gspread

CREDENTIALS_FILE = 'creds.json'

gc = gspread.service_account(filename=CREDENTIALS_FILE)
sh = gc.open("Приход/уход")

ws = sh.get_worksheet(0)


def append_record(record_data):
    ws.append_row(record_data)
