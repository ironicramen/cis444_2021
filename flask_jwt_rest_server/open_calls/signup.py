from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
#from tools.token_tools import create_token
from psycopg2 import sql
import bcrypt

from tools.logging import logger

cur = g.db.cursor()

def handle_request():
    logger.debug("Signup Handle Request")
    #use data here to auth the user
    password_from_user_form = request.form['password']
    
    user = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }

    userQuery = sql.SQL("SELECT * FROM {table} WHERE {pkey} ILIKE %s").format(
        table=sql.Identifier('users'),
        pkey=sql.Identifier('username'))

    cur.execute(userQuery, (user['sub'],))
    row = cur.fetchone()
   
    if row is None:
        logger.debug("Username Available")
        saltedPass = bcrypt.hashpw(bytes(request.form['password'], 'utf-8'), bcrypt.gensalt(12))
        utfSaltedPass = saltedPass.decode('utf-8')
        userInsertion = sql.SQL("INSERT INTO {table} ( {fields} ) VALUES (%s ,%s)").format(
            table = sql.Identifier('users'),
            fields = sql.SQL(', ').join([
                sql.Identifier('username'),
                sql.Identifier('password'),
            ]))

        data = ((user['sub'],), utfSaltedPass)
        cur.execute(userInsertion, data)
        g.db.commit()
        logger.debug("User Added, Database Commited")
        return json_response(status_=201, message = 'Username Created')
        
    else:
        logger.debug("Username Taken")
        return json_response(status_=401, message = 'Username In Use')


    

