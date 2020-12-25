from flask import Flask, render_template, request,redirect
from flask.globals import request
import gspread
import os
import json
from gspread.models import Worksheet
from oauth2client.client import Credentials
from oauth2client.service_account import ServiceAccountCredentials

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('prokiso-fd10525a5501.json',scope)
gc = gspread.authorize(credentials)
SPREADSHEET_KEY = '1eYy8_9XgbZjSWdPWX4wuruXKW3R6Cbv35wWILX_dyQc'
Worksheet = gc.open_by_key(SPREADSHEET_KEY)
SECRET_KEY = os.urandom(32)

app=Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# 検索フォームの設定
class SearchForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


@app.route('/')
def Hello():
    return 'HELLO'

@app.route('/register')
def register():
    page = request.args.get('circle')
    key_list = Worksheet.col_values(9) #query parameter
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
    key = Worksheet.cell(row_number,8).value #keywords to search
    lineId = Worksheet.cell(row_number,10).value
    webSite = Worksheet.cell(row_number,11).value
    twitterId = Worksheet.cell(row_number,12).value
    instagramId = Worksheet.cell(row_number,13).value
    mailAddress = Worksheet.cell(row_number,15).value
    otherWays = Worksheet.cell(row_number,14).value

    return render_template('index.html',
    name=name,
    genre=genre,
    space=space,
    univ=univ,
    intro=intro,
    key=key,
    lineId=lineId,
    webSite=webSite,
    twitterId=twitterId,
    instagramId=instagramId,
    mailAddress=mailAddress,
    otherWays=otherWays,)

@app.route('/submit', methods=('GET', 'POST'))
def search():
    form = SearchForm()
    if form.validate_on_submit():
        print(form.name)
        return redirect('/search_results/' + form.name.data)
    return render_template('submit.html', form=form)

@app.route('/search_results/<searchTerm>',methods=['GET', 'POST'])
def show_search_results(searchTerm):
    result = Worksheet.sheet1.findall(searchTerm)
    return render_template('hello.html', name1=result)

   

if __name__ == "__main__":
    app.run(debug=True)
