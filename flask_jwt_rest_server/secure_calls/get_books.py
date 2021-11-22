from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from psycopg2 import sql
from tools.logging import logger

cur = g.db.cursor()

def handle_request():
    logger.debug("Get Books Handle Request")

    bookQuery = sql.SQL("SELECT * FROM {table}").format(
        table = sql.Identifier('books'))

    cur.execute(bookQuery)
    bookQueryResult = cur.fetchall()
    return json_response( token = create_token(  g.jwt_data ) , books = bookQueryResult)

