from flask import Flask, render_template, request, jsonify, current_app
import requests
from flask_sqlalchemy import SQLAlchemy


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
    if request.method == 'POST':
        new_text = request.form['text-input']
        texthole = f"Запрос состояния трансформатора: {new_text}\n" + old_text
        # commit db
        text = Text(text=texthole)
        db.session.add(text)
        db.session.commit()
    return render_template('static/html/homepage.html', texthole=texthole)




if __name__ == '__main__':
    app.run(debug=True)


