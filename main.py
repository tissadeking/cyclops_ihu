import random
import string
from flask import Flask, render_template, redirect, request, jsonify
from mysql.connector import Error
from intent_compiler import intent_compiler_fun, intent_compiler_fun_2
from sparql_generator import sparql_generator_fun
import config
import sql_func

parameters = config.parameters
host = config.host
port = config.port
dc_port = config.dc_port
print("Application has started!", flush=True)

app = Flask(__name__, static_folder="static")

'''intent = {
    "intent_type": "",
    "fields": {
        "data": "",
        "parameter": "",
        "aggregate": "",
        "description": {
            "event": "",
            "reference": "",
            "sentiment": ""
        },
        "entity": "",
        "constraints": [],
        "influence": {
            "cause": "",
            "effect": ""
        },
        "location": {
            "main_location": "",
            "specific_location": ""
        },
        "time": "",
        "query": "",
        "intent_id": "",
        "userid": ""
    }
}'''

intent = {
    "intent_type": "",
    "fields": {}
}

#global field_data

# GET: Retrieve data
@app.route('/intent', methods=['GET'])
def get_fields():
    try:
        return jsonify(field_data), 200
    except:
        return jsonify(intent), 200

#PUT: Update data
@app.route('/intent', methods=['PUT'])
def update_field():
    global field_data
    data = request.get_json()
    field_data = data['fields']
    if data["intent_type"] == "exploratory":
        policy = intent_compiler_fun(field_data)
        answer = sparql_generator_fun(policy)
        # SEND A PUT OR POST REQUEST TO NLP CHAT WITH THE ANSWER
        # ANSWER has the userid, intent_id, df, df_columns,
        return jsonify({"answer": answer}), 200
    elif data["intent_type"] == "analytical":
        pipeline = intent_compiler_fun_2(field_data)
        #SEND A PUT OR POST REQUEST OF PIPELINE TO RUNTIME LAYER
        return jsonify({"pipeline": pipeline}), 200

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/enter", methods=["POST"])
def enter_fun():
    return render_template("login.html")

@app.route("/start")
def start_fun():
    return render_template("login.html")

@app.route("/signup")
def reg_fun():
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login_fun():
    username = request.form['username']
    password = request.form['password']
    existing_entry = sql_func.check_data(username, password)
    if existing_entry:
        #GET USER ID
        userid = sql_func.get_userid(username)
        chat_url = f"http://{host}:{dc_port}?userid={userid}"
        return redirect(chat_url)
    else:
        login_status = "Incorrect Username or Password"
        return render_template('login.html', login_text='Error: {}'.format(login_status))

@app.route("/register", methods=["POST"])
def register_fun():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    existing_email = sql_func.check_email(email)
    if existing_email:
        register_status = "Email already exists"
        return render_template('register.html', register_text='Error: {}'.format(register_status))
    else:
        existing_username = sql_func.check_username(username)
        if existing_username:
            register_status = "Username already exists"
            return render_template('register.html', register_text='Error: {}'.format(register_status))
        else:
            try:
                #GENERATE USER ID
                id_digits = 20
                url_safe_punctuation = "!$-_."
                charset = string.ascii_uppercase + string.digits + url_safe_punctuation
                userid = ''.join(random.choices(charset, k=id_digits))
                sql_func.insert_data(email, username, password, userid)
                return render_template("login.html")
            except Error as err:
                return render_template('register.html', register_text='Error: {}'.format(err))


if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)

