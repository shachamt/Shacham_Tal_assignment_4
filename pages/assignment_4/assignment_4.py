from flask import Blueprint, render_template
from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector

assignment_4 = Blueprint('assignment_4', __name__,
                  static_folder='static',
                  template_folder='templates')

@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    user_id = request.form['user_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['user_email']
    password = request.form['password']
    user_name = request.form['user_name']
    print(f'{user_name} {user_id} {first_name} {last_name} {password}')
    query = "INSERT INTO users(user_id, first_name, last_name, email, password, user_name) VALUES ('%s','%s','%s','%s','%s','%s')" % (user_id, first_name, last_name, email, password, user_name)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')

@assignment_4.route('/assignment_4')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment_4.html', users=users_list)


def interact_db(query, query_type: str):
        return_value = False
        connection = mysql.connector.connect(host='localhost',
                                             user='root',
                                             passwd='root',
                                             database='assignment_4')
        cursor = connection.cursor(named_tuple=True)
        cursor.execute(query)
        #

        if query_type == 'commit':
            # Use for INSERT, UPDATE, DELETE statements.
            # Returns: The number of rows affected by the query (a non-negative int).
            connection.commit()
            return_value = True

        if query_type == 'fetch':
            # Use for SELECT statement.
            # Returns: False if the query failed, or the result of the query if it succeeded.
            query_result = cursor.fetchall()
            return_value = query_result

        connection.close()
        cursor.close()
        return return_value
