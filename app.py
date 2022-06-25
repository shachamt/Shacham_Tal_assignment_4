from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector

app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)


from pages.assignment_4.assignment_4 import assignment_4
app.register_blueprint(assignment_4)

@app.route('/')
def hello_world():  # put application's code here
    return render_template('assignment_4.html')

@app.route('/session')
def session_func():
    # print(session['CHECK'])
    return jsonify(dict(session))


# ------------------------------------------------- #
# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #
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
@app.route('/users')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment_4.html', users=users_list)

if __name__ == '__main__':
    app.run(debug=True)

# INSERT INTO users(user_ID,first_name,last_name,email,user_name,password) VALUES (313131317,'aviv','menahem','aviv@post.bgu.ac.il','avivM','8585')
# INSERT INTO users(user_ID,first_name,last_name,email,user_name,password) VALUES (258471369,'adi','mizrahi','adimi@post.bgu.ac.il','adidi','3641')
# INSERT INTO users(user_ID,first_name,last_name,email,user_name,password) VALUES (285236581,'shir','yehezkel','shishir@post.bgu.ac.il','shirshir','2258')