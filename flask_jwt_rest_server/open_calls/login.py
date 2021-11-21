from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from psycopg2 import sql
import bcrypt

from tools.logging import logger

cur = g.db.cursor()

def handle_request():
    logger.debug("Login Handle Request")
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
   
    if row is not None:
        logger.debug("User found")
        saltedPass = bytes(row[2],'utf-8')
        checkPassword = bcrypt.checkpw(bytes(request.form['password'], 'utf-8'),saltedPass)

        if(checkPassword):
            logger.debug("Password Match")
            return json_response( token = create_token(user) , authenticated = True)
        
        else:
            logger.debug("Password Not Match")
            return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )

    else:
        logger.debug("User not Found")
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )


    

