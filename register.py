from flask import Flask, render_template
from flask.globals import request
import gspread
import json
from gspread.models import Worksheet
from oauth2client.client import Credentials
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('prokiso-fd10525a5501.json',scope)
gc = gspread.authorize(credentials)
SPREADSHEET_KEY = '1eYy8_9XgbZjSWdPWX4wuruXKW3R6Cbv35wWILX_dyQc'
Worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet("Sheet1")

app=Flask(__name__)

@app.route('/')
def Hello():
    return 'HELLO'

@app.route('/register')
def register():
    page = request.args.get('circle')
    key_list = Worksheet.col_values(9)
    row_number = -1
    for i, key in enumerate(key_list):
        if key == page:
            row_number = i
            break
    name = Worksheet.cell(row_number,2).value
    genre = Worksheet.cell(row_number,3).value
    space = Worksheet.cell(row_number,4).value
    univ = Worksheet.cell(row_number,5).value
    intro = Worksheet.cell(row_number,6).value
    key = Worksheet.cell(row_number,8).value
    return render_template('index.html',name=name,genre=genre,space=space,univ=univ,intro=intro,key=key)

if __name__ == "__main__":
    app.run(debug=True)
