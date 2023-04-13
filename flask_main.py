import datetime

from flask import Flask, render_template, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from loggingGenerator import hourly_message


app = Flask(__name__, static_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())

with app.app_context():
    db.create_all()



@app.route('/', methods=['GET', 'POST'])
def index():
    last_text = Text.query.order_by(Text.id.desc()).first()
    old_text = last_text.text if last_text else ""
    print("oldtext", old_text)
    current_datetime = datetime.datetime.now()
    month = current_datetime.month
    minute = current_datetime.minute
    if len(str(month)) == 1:
        month = f'0{str(month)}'
    if len(str(minute)) == 1:
        minute = f'0{str(minute)}'
    verdict_time = f'{current_datetime.day}.{month}.{current_datetime.year} {current_datetime.hour}:{minute}'

    texthole = ""
    if request.method == 'POST':
        new_text = request.form['text-input']
        print("newtext =", new_text)




        texthole = f'<a>Запрос состояния трансформатора {new_text}:</a> <a style="color: cyan">{verdict_time}</a> {hourly_message(-5, 20, 20, 20, 20)[0]}<br>' + old_text
        # commit db
        text = Text(text=texthole)
        db.session.add(text)
        db.session.commit()
    return render_template('static/html/homepage.html', texthole=texthole)




if __name__ == '__main__':
    app.run(debug=True)


