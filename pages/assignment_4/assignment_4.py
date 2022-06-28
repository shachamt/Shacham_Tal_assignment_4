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
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['user_email']
    password = request.form['password']
    user_name = request.form['user_name']
    query = "INSERT INTO users(first_name, last_name, email, password, user_name) VALUES ('%s','%s','%s','%s','%s')" % ( first_name, last_name, email, password, user_name)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')

@assignment_4.route("/update_first_name", methods=['POST'])
def update_first_name():
    user_id = request.form['user_id']
    print(user_id)

    first_name = request.form['first_name']
    query = "UPDATE users \
            SET first_name= '%s' \
            WHERE user_id= '%s';" %(first_name,user_id)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')

@assignment_4.route("/update_last_name", methods=['POST'])
def update_last_name():
    user_id = request.form['user_id']
    last_name = request.form['last_name']
    query = "UPDATE users \
            SET last_name= '%s' \
            WHERE user_id= '%s';" %(last_name,user_id)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')

@assignment_4.route("/update_email", methods=['POST'])
def update_email():
    user_id = request.form['user_id']
    email = request.form['email']
    query = "UPDATE users \
            SET email= '%s' \
            WHERE user_id= '%s';" %(email,user_id)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')

@assignment_4.route("/update_user_name", methods=['POST'])
def update_user_name():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    query = "UPDATE users \
            SET user_name= '%s' \
            WHERE user_id= '%s';" %(user_name,user_id)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')

@assignment_4.route("/update_password", methods=['POST'])
def update_password():
    user_id = request.form['user_id']
    password = request.form['password']
    query = "UPDATE users \
            SET password= '%s' \
            WHERE user_id= '%s';" %(password,user_id)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')


@assignment_4.route("/delete_user", methods=['POST'])
def delete_user():
    user_id = request.form['user_id']
    print(user_id)
    query = "DELETE FROM users WHERE user_id= '%s';" %user_id
    interact_db(query, query_type='commit')
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
