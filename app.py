from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector
import requests
import time
import os
from dotenv import load_dotenv

app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)


from pages.assignment_4.assignment_4 import assignment_4
app.register_blueprint(assignment_4)

@app.route('/')
def hello_world():  # put application's code here
    return redirect('/assignment_4')

@app.route('/session')
def session_func():
    # print(session['CHECK'])
    return jsonify(dict(session))


# ------------------------------------------------- #
# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #


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

# query = "INSERT INTO try_table_1(name) VALUES ('try_name_1')"
# interact_db(query=query, query_type='commit')
#
# query = "select * from try_table_1"
# query_result = interact_db(query=query, query_type='fetch')
# print(query_result)
# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# ------------------- SELECT ---------------------- #
# ------------------------------------------------- #
@app.route('/assignment4/users')
def assignment4_users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return_list = []
    for user in users_list:
        user_dict = {
                       'first_name': user.first_name,
                       'last_name': user.last_name,
                       'email': user.email,
                       'user_name': user.user_name
                       }
        return_list.append(user_dict)
    return jsonify(return_list)

@app.route('/assignment4/outer_source')
def assignment4_outer_source():
    return render_template('outer_source.html')

@app.route('/fetch_be')
def fetch_be():
    if 'type' in request.args:
        print('after click')
        id= request.args['id']
        users = []
        res = requests.get('https://reqres.in/api/users/' +id)
        users.append(res.json())

        user_dict= {
            'first_name': users[0]['data']['first_name'],
            'last_name': users[0]['data']['last_name'],
            'email': users[0]['data']['email'],
            'avatar': users[0]['data']['avatar'],
        }

    return render_template('outer_source.html',first_name=user_dict['first_name'],
                           last_name=user_dict['last_name'],
                           email=user_dict['email'],
                           avatar=user_dict['avatar'])


@app.route('/assignment4/restapi_users', defaults={'USER_ID': 6})
@app.route('/assignment4/restapi_users/<int:USER_ID>')
def restapi_users(USER_ID):
    query = f'select * from users where user_id={USER_ID}'
    user_list = interact_db(query, query_type='fetch')

    if len(user_list) ==0:
        return_dict= {
            'message': 'user not found'
        }
    else:
        user_list=user_list[0]
        return_dict = {'first_name': user_list.first_name,
                       'last_name': user_list.last_name,
                       'email': user_list.email,
                       'user_name': user_list.user_name}
    return jsonify(return_dict)

if __name__ == '__main__':
    app.run(debug=True)


#INSERT INTO users(first_name,last_name,email,user_name,password) VALUES ('aviv','menahem','aviv@post.bgu.ac.il','avivM','8585')
#INSERT INTO users(first_name,last_name,email,user_name,password) VALUES ('adi','mizrahi','adimi@post.bgu.ac.il','adidi','3641')
#INSERT INTO users(first_name,last_name,email,user_name,password) VALUES ('shir','yehezkel','shishir@post.bgu.ac.il','shirshir','2258')
#INSERT INTO users(first_name,last_name,email,user_name,password) VALUES ('shacham','tal','shachamt@post.bgu.ac.il','shachamt','1345')
#INSERT INTO users(first_name,last_name,email,user_name,password) VALUES ('nir','yaakov','nirnir@post.bgu.ac.il','niro','2222')
