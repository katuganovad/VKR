import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from create_model import db, Protocol, Teams, Referees, Authorize, Players
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1703@localhost/KFV'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Декоратор для проверки аутентификации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Требуется вход в систему.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        fio = request.form.get('fio')
        password = request.form.get('password')
        user = Authorize.query.filter_by(fio=fio, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('add_protocol_step1'))  # Перенаправление на первую страницу добавления протокола
        else:
            flash('Неверный логин или пароль.')

    # Получаем всех пользователей при GET-запросе для выпадающего списка
    users = Authorize.query.all()  # Загрузка всех пользователей
    return render_template('login.html', users=users)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/add_protocol_step1', methods=['GET', 'POST'])
@login_required
def add_protocol_step1():
    teams = Teams.query.all()
    referees = Referees.query.all()
    success_message = ""
    error_message = ""

    if request.method == 'POST':
        try:
            # Получение данных формы
            competition_name = request.form['competition_name']
            city = request.form['city']
            hall = request.form['hall']
            stage = request.form['stage']
            match = int(request.form['match'])
            gender = request.form['gender']
            category = request.form['category']
            date_str = request.form['date']
            time_str = request.form['time']
            team1 = int(request.form['team1'])
            team2 = int(request.form['team2'])
            secretary = int(request.form['secretary'])
            referee = int(request.form['referee'])

            # Сохраним данные в сессии
            session['competition_name'] = competition_name
            session['city'] = city
            session['hall'] = hall
            session['stage'] = stage
            session['match'] = match
            session['gender'] = gender
            session['category'] = category
            session['date'] = date_str
            session['time'] = time_str
            session['team1'] = team1
            session['team2'] = team2
            session['secretary'] = secretary
            session['referee'] = referee

            # Перенаправление на вторую страницу
            return redirect(url_for('add_protocol_step2'))

        except Exception as e:
            error_message = f'Ошибка добавления протокола: {e}'

    return render_template('add_protocol_page1.html', teams=teams, referees=referees,
                           success=success_message, error=error_message)

@app.route('/add_protocol_step2', methods=['GET', 'POST'])
@login_required
def add_protocol_step2():
    if request.method == 'POST':
        # Здесь можно обрабатывать данные для протокола
        # Сохраните собранные данные и перейдите к следующему шагу
        return redirect(url_for('finalize_protocol'))  # Перенаправление на финализацию протокола

    return render_template('add_protocol_page2.html')

@app.route('/finalize_protocol', methods=['GET', 'POST'])
@login_required
def finalize_protocol():
    # Здесь вы можете обработать сохранение протокола
    return render_template('finalize_protocol.html')

@app.route('/download_protocol/<path:filename>')
def download_protocol(filename):
    return send_file(filename, as_attachment=True)

@app.route('/search_protocols', methods=['GET', 'POST'])
def search_protocols():
    protocols = []
    if request.method == 'POST':
        search_date = request.form['search_date']
        date_object = datetime.strptime(search_date, "%Y-%m-%d").date()
        protocols = Protocol.query.filter(Protocol.date == date_object).all()
    return render_template('search_protocols.html', protocols=protocols)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
