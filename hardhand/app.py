from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from bson import ObjectId
from pymongo import MongoClient
from flask import jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import requests
import time
import json

data_to_display = None

app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Připojení k MongoDB
client = MongoClient('mongodb://localhost:27017/')
mongodb = client['zptest']
collection = mongodb['users']

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    @staticmethod
    def get_role_level(role_name):
        roles_order = ['admin', 'verified', 'unverified', 'ban']  # Od nejvyšší do nejnižší
        return roles_order.index(role_name) if role_name in roles_order else -1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role_level = db.Column(db.Integer, default=0)  # Default role level
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))


# Následující kód by měl být kdesi v inicializační části vaší aplikace
class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

from functools import wraps

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        first_user = User.query.first()
        if first_user:
            if 'user_id' not in session:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        else:
            return redirect(url_for('firstuser'))
    return decorated_function

def role_required(minimum_role_level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))

            user = User.query.get(session.get('user_id'))
            if not user or user.role_level < minimum_role_level:
                return redirect(url_for('unverified'))

            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_user_role():
    user_id = session.get('user_id')
    
    if user_id:
        user = User.query.get(user_id)
        if user:
            return user.roles[0].name if user.roles else None

    return None

def verifie_role():
    roles_order = ['ban', 'unverified', 'verified', 'admin']  # Od nejvyšší do nejnižší
    role = get_user_role()
    for number in range(len(roles_order)):
        if roles_order[number] == role:
            check = number
            return check
    

@app.route('/')
@login_required
# @role_required(1)  # Změňte na požadovaný minimální level role
def index():
    first_user = User.query.first()
    if first_user:
        # Pokud existuje alespoň jeden uživatel v databázi, přesměrujte na hlavní stránku
        # Získání všech dokumentů z kolekce
        mongo_data = list(collection.find({}, {"_id": 1, "username": 1, "password": 1}))
        check = verifie_role()
        if int(check) == 0:
            return redirect(url_for('ban'))
        elif int(check) == 1:
            return redirect(url_for('unverified'))
        role = get_user_role()

        return render_template('home.html', mongo_data=mongo_data, role=role)
    else:
        # Pokud v databázi neexistuje žádný uživatel, přesměrujte na stránku pro registraci
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password)
            new_user.roles.append(Role(name='admin')) # probably use unverified (not for here)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        
        return render_template('firstuser.html')
        
    
"""
@app.route('/firstrun', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            # Uživatel je v databázi, přihlásíme ho
            return 'Uživatel je v databázi.', 200
        else:
            # Uživatel není v databázi, zobrazíme mu formulář pro registraci
            return redirect(url_for('register'))
    return render_template('index.html')
"""

@app.route('/update_row', methods=['POST'])
@login_required
def update_row():
    row_id = request.form.get('id')
    username = request.form.get('username')

    password = request.form.get('password')

    # Převedení řetězce na ObjectId
    row_id = ObjectId(row_id)

    # Aktualizace řádku v MongoDB
    collection.update_one({'_id': row_id}, {'$set': {'username': username, 'password': password}})

    # Přesměrování zpět na hlavní stránku
    return redirect(url_for('index'))

@app.route('/delete_row', methods=['POST'])
@login_required
def delete_row():
    row_id = request.form.get('id')

    # Převedení řetězce na ObjectId
    row_id = ObjectId(row_id)

    # Odebrání řádku z MongoDB
    collection.delete_one({'_id': row_id})

    # Přesměrování zpět na hlavní stránku
    return redirect(url_for('index'))

@app.route('/delete_record/<string:record_id>', methods=['DELETE'])
@login_required
def delete_record(record_id):
    try:
        # Převedení řetězce na ObjectId
        row_id = ObjectId(record_id)

        # Odebrání řádku z MongoDB
        collection.delete_one({'_id': row_id})

        return jsonify({'success': True, 'message': 'Záznam byl úspěšně odstraněn.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/update_record/<string:record_id>', methods=['PUT'])
@login_required
def update_record(record_id):
    try:
        data = request.get_json()
        record_id = ObjectId(record_id)

        # Aktualizace záznamu v MongoDB
        collection.update_one({'_id': record_id}, {'$set': {'username': data['username'], 'password': data['password']}})

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password.'
            #error = User.query.filter_by(username=username).first()
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/unverified')
@login_required
def unverified():
    return render_template('unverified.html')  # Zde můžete přidat vlastní šablonu nebo logiku pro neověřené uživatele

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            error = 'Username already exists. Please choose a different one.'
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password)
            new_user.roles.append(Role(name='unverified')) # probably use unverified
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    
    return render_template('register.html', error=error)

@app.route('/admin')
@login_required
def admin_page():
    role = get_user_role()
    if role == 'admin':
        return render_template('admin.html')
    else:
        return render_template('unauthorized.html')

@app.route('/process_request', methods=['POST'])
def process_request():
    url = "http://127.0.0.1:8000/run_python_code"
    # Získání dat z POST požadavku v JSON formátu
    data = request.get_json()
    button_id = data.get('buttonId', '')

    # Zpracování a výpis do konzole
    print(f"Server B received a request from button with ID: {button_id}")

    if button_id == "active-button-login":
        data = {"what_now": "g"}  # Změňte hodnotu dle potřeby
    elif button_id == "active-button-error":
        data = {"what_now": "b"}  # Změňte hodnotu dle potřeby
    elif button_id == "active-button-2fa":
        data = {"what_now": "y"}  # Změňte hodnotu dle potřeby
    else:
        return jsonify(message="Server B processed the request.")

    response = requests.post(url, params=data)
    print(response.json())
    return jsonify(message="Server B processed the request.")

@app.route('/data_reciever_sse', methods=['POST'])
def data_reciever_sse():
    # Získání dat z POST požadavku
    twofa = request.form.get('2fa')
    username = request.form.get('username')
    password = request.form.get('password')
    print(username, password)
    print(twofa)
    global data_to_display
    data_to_display = [username, password, twofa]

@app.route('/status_recieve', methods=['POST'])
def status_recieve():
    global new_data
    # Získání dat z POST požadavku
    status = request.form.get('status')
    print(status)
    global status_to_display
    status_to_display = status
    new_data = True
    return "good"

# SSE funkce - tato funkce bude posílat aktualizace klientovi
def generate_sse():
    global new_data
    if new_data:
        global status_to_display
        global data_to_display
        try:
            data_to_display ={"username": data_to_display[0], "password": data_to_display[1], "2fa": data_to_display[2], "status": status_to_display}
        except:
            data_to_display ={"status": status_to_display}
        yield f"data: {data_to_display}\n\n"
        print(data_to_display)
        time.sleep(1)
        new_data = False


# Endpoint pro SSE
@app.route('/stream')
def stream():
    return Response(generate_sse(), content_type='text/event-stream')

@app.route('/test')
def test():
    return render_template('test.html')

# Inicializace status_to_display
status_to_display = {"status": "initial_value"}

"""
def status_recieve_generate():
    global status_to_display
    print("done")
    print(status_to_display)
    yield f"data: {json.dumps(status_to_display)}\n\n"

@app.route('/stream_status')
def stream_status():
    return Response(status_recieve_generate(), content_type='text/event-stream')
"""

@app.route('/firstuser', methods=['POST', 'GET'])
def firstuser():
    first_user = User.query.first()
    if first_user:
        return redirect(url_for('home'))
    else:
        # Pokud v databázi neexistuje žádný uživatel, přesměrujte na stránku pro registraci
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password)
            new_user.roles.append(Role(name='admin')) # probably use unverified (not for here)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        
        return render_template('firstuser.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=2222, debug=True)
