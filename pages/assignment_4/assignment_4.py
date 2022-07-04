from flask import Blueprint, render_template
from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector
import os

assignment_4 = Blueprint('assignment_4', __name__,
                  static_folder='static',
                  template_folder='templates')

@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    email = request.form['user_email']
    user_name = request.form['user_name']
    for user in users_list:
        if email == user.email:
            return render_template('assignment_4.html',users=users_list, existMessage="Email already exists in system!")
        if user_name == user.user_name:
            return render_template('/assignment_4.html',users=users_list, existMessage="User name already exists in system!")

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    query = "INSERT INTO users(first_name, last_name, email, password, user_name) VALUES ('%s','%s','%s','%s','%s')" % ( first_name, last_name, email, password, user_name)
    interact_db(query=query, query_type='commit')
    return render_template('/assignment_4.html', users=users_list, successMessage="User added successfully!")

@assignment_4.route("/identify", methods=['POST'])
def identify():
    user_name = request.form['user_name']
    password = request.form['password']
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')

    for user in users_list:
        if user_name == user.user_name:
            if password == user.password:
                return render_template('assignment_4.html', users=users_list, user=user)
            else:
                return render_template('assignment_4.html', wrongMessage='Wrong Password')
    return render_template('assignment_4.html', wrongMessage='Wrong User Name')

@assignment_4.route("/update", methods=['POST'])
def update():
    user_name = request.form['user_name']
    user_id = request.form['user_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    query = 'select * from users'
    query2 = 'select * from users' \
             'where user_id=user_id'
    users_list = interact_db(query, query_type='fetch')
    currUser = interact_db(query, query_type='fetch')

    if user_name!='':
        for user in users_list:
            if user_name == user.user_name:
                return render_template('assignment_4.html',exist="User Name already exists in system!",user=currUser,users=users_list)
        query = "UPDATE users \
                SET user_name= '%s' \
                WHERE user_id= '%s';" % (user_name, user_id)
        interact_db(query=query, query_type='commit')

    if first_name!='':
        query = "UPDATE users \
                SET first_name= '%s' \
                WHERE user_id= '%s';" % (first_name, user_id)
        interact_db(query=query, query_type='commit')

    if last_name != '':
        query = "UPDATE users \
                SET last_name= '%s' \
                WHERE user_id= '%s';" % (last_name, user_id)
        interact_db(query=query, query_type='commit')

    if email != '':
        for user in users_list:
            if email == user.email:
                return render_template('assignment_4.html',exist="Email already exists in system!",user=currUser,users=users_list)
        query = "UPDATE users \
                SET email= '%s' \
                WHERE user_id= '%s';" % (email, user_id)
        interact_db(query=query, query_type='commit')

    if password != '':
        query = "UPDATE users \
                SET password= '%s' \
                WHERE user_id= '%s';" % (password, user_id)
        interact_db(query=query, query_type='commit')

    if (password == '') & (email == '') & (last_name == '') &(first_name=='') & (user_name==''):
        return render_template('assignment_4.html', done='Nothing to update', users=users_list)

    return render_template('assignment_4.html', done='Updated',users=users_list)

@assignment_4.route("/delete_user", methods=['POST'])
def delete_user():
    user_id = request.form['user_id']
    print(user_id)
    query = "DELETE FROM users WHERE user_id= '%s';" %user_id
    interact_db(query, query_type='commit')
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment_4.html', users=users_list, delete='User deleted')

@assignment_4.route('/assignment_4')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment_4.html', users=users_list)


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host=os.getenv('DB_HOST'),
                                         user=os.getenv('DB_USER'),
                                         passwd=os.getenv('DB_PASSWORD'),
                                         database=os.getenv('DB_NAME'))
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
