import datetime
import random
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
    list_of_transformers = ["000001", "PETROZAVODSK", "IRSA", '230606'] # условный список существующий трансформаторов !!!! Принимает только str тк new_text тоже str
    texthole= ""

    if request.method == 'POST':
        new_text = request.form['text-input']
        if new_text != "":
            if new_text in list_of_transformers:
                ph_level, temperature, knockouts_number, shutdowns_number, overloads_number = 30, 30, 30, 30, 3
                hh, dd = 20, 34
                if new_text == list_of_transformers[0]:
                    ph_level = 5
                    dd = 15
                elif new_text == list_of_transformers[1]:
                    ph_level = -5
                    hh, dd = 9, 15
                elif new_text == list_of_transformers[2]:
                    ph_level, temperature = -5, 5
                    hh, dd = 6, 8
                answer = hourly_message(ph_level, temperature, knockouts_number, shutdowns_number, overloads_number, hh, dd)
                texthole = f'<a>Запрос состояния трансформатора {new_text}:</a> <a style="color: cyan">{verdict_time}</a> {answer}<br>' + old_text
                # commit db
                text = Text(text=texthole)
                db.session.add(text)
                db.session.commit()
                return render_template('static/html/homepage.html', texthole=texthole)

            else: #трансформатора не существует или мы его не нашли\

                flash(f'Трансформатор "{new_text}" не найден в списке.')
                return render_template('static/html/homepage.html', texthole=old_text)
        else:
            texthole = Text(text=texthole)


    return render_template('static/html/homepage.html', texthole=old_text)

# TODO: Сделать кнопку неактивной при пустом поле
# TODO: если введённые данные не int возвращать ошибку | если такого трансформатора не существует
# todo: если бутстрап пустой то можно ли потом из кода взять его и сделать типо наполненным написать сказку
# <div class="alert alert-warning d-flex align-items-center" role="alert">
#   <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Warning:"><use xlink:href="#exclamation-triangle-fill"/></svg>
#   <div>
#     Пример уведомления предупреждения с иконкой
#   </div>

@app.route('/clear-table', methods=['POST'])
def clear_table():
    # очищаем таблицу в базе данных с помощью SQLAlchemy
    db.session.query(Text).delete()
    db.session.commit()

    # возвращаем JSON-ответ клиенту
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


