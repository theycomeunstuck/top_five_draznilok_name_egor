import datetime

from flask import Flask, render_template, redirect, request, jsonify, current_app, flash
from flask_sqlalchemy import SQLAlchemy
from loggingGenerator import hourly_message




app = Flask(__name__, static_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'secret_key'
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
    current_datetime = datetime.datetime.now()
    month = current_datetime.month
    minute = current_datetime.minute
    if len(str(month)) == 1:
        month = f'0{str(month)}'
    if len(str(minute)) == 1:
        minute = f'0{str(minute)}'
    verdict_time = f'{current_datetime.day}.{month}.{current_datetime.year} {current_datetime.hour}:{minute}'
    list_of_transformers = ["1","2","3","4","5","6","7","8", "12" ,"xxx", "ddd","aaa","transformer"] # условный список существующий трансформаторов !!!! Принимает только str тк new_text тоже str
    texthole= ""

    if request.method == 'POST':
        new_text = request.form['text-input']
        if new_text != "":
            if new_text in list_of_transformers:
                texthole = f'<a>Запрос состояния трансформатора {new_text}:</a> <a style="color: cyan">{verdict_time}</a> {hourly_message(-5, 20, 20, 20, 20)[0]}<br>' + old_text
                # commit db
                text = Text(text=texthole)
                db.session.add(text)
                db.session.commit()
                return render_template('static/html/homepage.html', texthole=texthole)

            else: #трансформатора не существует или мы его не нашли\
                flash('Такого нет')
                return render_template('static/html/homepage.html', texthole=texthole)
        else:
            texthole = Text(text=texthole)
    return render_template('static/html/homepage.html', texthole=texthole, notification=notification)
    # return render_template('static/html/homepage.html', texthole=texthole)
    # return redirect('static/html/homepage.html', texthole=texthole)
# TODO: Сделать кнопку неактивной при пустом поле
# TODO: если введённые данные не int возвращать ошибку | если такого трансформатора не существует
# todo: если бутстрап пустой то можно ли потом из кода взять его и сделать типо наполненным написать сказку
# <div class="alert alert-warning d-flex align-items-center" role="alert">
#   <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Warning:"><use xlink:href="#exclamation-triangle-fill"/></svg>
#   <div>
#     Пример уведомления предупреждения с иконкой
#   </div>
if __name__ == '__main__':
    app.run(debug=True)


