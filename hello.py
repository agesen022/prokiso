from flask import Flask, render_template, request,redirect #追加
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import gspread
import os
SECRET_KEY = os.urandom(32)


gc = gspread.service_account("./prokiso-fd10525a5501.json")
sh = gc.open("サークル登録用（回答）")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

class SearchForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

@app.route('/')
def hello():
    name = "Hoge"
    circle_name = 'robotech'
    name = sh.sheet1.get('B2')
    return render_template('hello.html', title='flask test', name1=name, circle_name=circle_name) #変更

@app.route('/calendar')
def calendar():
    return render_template('calendar.html', title='flask test') #変更

@app.route('/submit', methods=('GET', 'POST'))
def search():
    form = SearchForm()
    if form.validate_on_submit():
        print(form.name)
        return redirect('/search_results/' + form.name.data)
    return render_template('submit.html', form=form)

@app.route('/search_results/<searchTerm>',methods=['GET', 'POST'])
def show_search_results(searchTerm):
    result = sh.sheet1.findall(searchTerm)
    return render_template('hello.html', name1=result)

if __name__ == "__main__":
    app.run(debug=True)