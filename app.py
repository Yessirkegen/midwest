from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'beksultanestirkegen@gmail.com'
app.config['MAIL_PASSWORD'] = 'egbz pwkw jabj yrcr'
app.config['MAIL_DEFAULT_SENDER'] = 'beksultanestirkegen@gmail.com'

mail = Mail(app)
db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    service = db.Column(db.String(100))  # Новое поле для типа услуги
    message = db.Column(db.Text, nullable=False)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')  # Получаем тип услуги
        message = request.form.get('message')

        # Создание и сохранение данных формы
        form_data = FormData(name=name, email=email, phone=phone, service=service, message=message)
        db.session.add(form_data)
        db.session.commit()

        # Отправка письма
        send_email(name, email, phone, service, message)

        return jsonify({"status": "success"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error"})

def send_email(name, email, phone, service, message):
    subject = 'New Form Submission'
    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nService Type: {service}\nMessage: {message}"

    msg = Message(subject, recipients=['beksultanestirkegen@gmail.com'])
    msg.body = body
    mail.send(msg)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)