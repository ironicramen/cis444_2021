
from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import datetime
import bcrypt


from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = None

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    print(request.form)
    salted = bcrypt.hashpw( bytes(request.form['fname'],  'utf-8' ) , bcrypt.gensalt(10))
    print(salted)

    print(  bcrypt.checkpw(  bytes(request.form['fname'],  'utf-8' )  , salted ))

    return render_template('backatu.html',input_from_browser= str(request.form) )

@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)



#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )

@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] } 
                            , JWT_SECRET, algorithm="HS256")
    #print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    global_db_con.commit()
    return json_response(status="good")


#### Assignment 3 ####


@app.route('/userlogin', methods=['POST']) #user login endpoint
def userlogin():
    cur = global_db_con.cursor()
    u = request.form['username']
    cur.execute(f"SELECT password FROM users WHERE username = '{u}';")
    p = cur.fetchone()[0]
    if(p == None):
        print("User not in database")
        return "FALSE"
    else:
        p = bytes(p,'utf-8')
        checkP = bcrypt.checkpw(bytes(request.form['password'], 'utf-8'),p)
        if(checkP):
            jwt_str = jwt.encode({"username" : u}, JWT_SECRET, algorithm="HS256")
            return json_response(jwt=jwt_str)
        else:
            print("No password match!")
            return "FALSE"
    
@app.route( '/userSignUp', methods=['POST']) #user signup endpoint
def userSignUp():
    u = request.form['new_username'] #username variable from user input
    today = datetime.datetime.now()
    strdate = today.strftime('%Y-%m-%d')
    cur = global_db_con.cursor() #database cursor
    cur.execute(f"SELECT * FROM users WHERE username = '{u}';")
    if cur.fetchone() == None: # 
        saltyP = bcrypt.hashpw(bytes(request.form['new_password'], 'utf-8'), bcrypt.gensalt(10))
        unsaltyP = saltyP.decode('utf-8')
        print(unsaltyP)
        print(strdate)
        cur.execute(f"INSERT INTO users (username, password, acct_date, recent_act) VALUES ('{u}', '{unsaltyP}', '{strdate}', 'FALSE');")
        global_db_con.commit()
        jwt_str = jwt.encode({"username" : u}, JWT_SECRET, algorithm="HS256")
        return json_response(jwt=jwt_str)
    else:
        print("Username Taken")
        return "FALSE"


app.run(host='0.0.0.0', port=80)
