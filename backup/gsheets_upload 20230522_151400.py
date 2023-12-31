from classes import *
import ast

gsheets = GoogleSheets()

while True:
    time.sleep(1)
    if os.path.exists(gsheets.localspreadsheet):
        print('UPDATING TO GOOGLE SHEETS')
        with open(gsheets.localspreadsheet, 'r', encoding='utf-8') as f:
            file_contents = f.read()
        file_contents = ast.literal_eval(file_contents)
        if gsheets.append(file_contents):
            os.remove(gsheets.localspreadsheet)
            print('UPDATED TO GOOGLE SHEETS')
        else:
            print('FAILED TO UPDATE TO GOOGLE SHEETS')
    else:
        print('File not exist')
        pass
