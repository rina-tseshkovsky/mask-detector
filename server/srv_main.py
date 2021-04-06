from bottle import run, get, post, request, delete, route, template
import sqlite3
import os.path

#to write a route for login

@post('/send_buffer')
def accept_data():
    print("debug accept data")
    buffer = request.json['buffer']
    conn = sqlite3.connect('masking.db')
    #c = cursor
    c = conn.cursor()
    for block in buffer:
        id = block['id']
        date = block['date']
        status = block['status']
        print("DEBUG: " + id + ", " + date + ", " + status)
        c.execute("INSERT INTO raw_data(ID, DATE, STATUS) VALUES(?, ?, ?)", (id, date, status))
        conn.commit()
    conn.close()

@route('/main')
def main_menu():
    print("entering main route")
    return template('main.tpl')

#main tpl
@route('/main', method = "post")
def do_main_menu():
    if request.forms.get('bt1') == "Users" :
        return template('users.tpl')
    if request.forms.get('bt2') == "Sensors" :
        return template('sensors.tpl')
    if request.forms.get('bt3') == "SQL Request" :
        print("reached sql request")
        return template('sql-request.tpl')
    if request.forms.get('bt4') == "DB Opse" :
        print("reached db-opse.tpl")
        return template('db-opse.tpl')

#users tpl
@route('/users', method = "post")
def do_users_menu():
    if request.forms.get('bt1') == "Add User" :
        return template('add-user.tpl', usr_id=222)
    elif request.forms.get('bt2') == "Delete User" :
        print("reached delete user")
        return template('delete-user.tpl',  usr_id=222)
    elif request.forms.get('bt3') == "Show All Users" :
        return template('show-all-users.tpl')
    elif request.forms.get('bt4') == "Back" :
        return template('main.tpl')
    else:
        print("Wrong selection")


@get('/test')
def test():
    print("entering test")
    my_status = "2"
    cou = 0
    #select status from row_data table
    conn = sqlite3.connect('masking.db')
    c = conn.cursor()
    c.execute("SELECT * FROM raw_data WHERE status=?", (my_status))
    rows = c.fetchall()
    for row in rows:
        print(row[1])
        cou = cou + 1
    return template('templae-test3.tpl', tpl_tows=rows)
    #return template('template-test2.tpl', h_cou = cou, h_status = my_status)

@route('/sql-request')
def sql_request():
    return '''
        <form action="/sql-request" method="post">
            Input SQL query: <input name="sql-query" type="text" />
            <input value="SQL Rrequest1" type="submit" />
        </form>   
    '''

@route('/sql-request', method='POST')
def do_sql_request():
    sql_query = request.forms.get('sql-query')
    conn = sqlite3.connect('masking.db')
    c = conn.cursor()
    c.execute(sql_query)
    rows = c.fetchall()
    #for row in rows:
        #print(row[1])
    return template('templae-test3.tpl', tpl_tows=rows)

def initialize():
    if os.path.isfile('masking.db'):
        print("the database already exists")
    else:
        print("creating the database")
        conn = sqlite3.connect('masking.db')
        c = conn.cursor()
        c.execute("CREATE TABLE raw_data(id INTEGER, date TEXT, status INTEGER)")
        c.execute("CREATE TABLE users(id INTEGER, name TEXT, password INTEGER)")
        #c.execute("CREATE TABLE sensors(id INTEGER, date TEXT, status INTEGER)")

        conn.close() 

    #יוצרת DB במידה והאו לא קיים



if __name__ == '__main__':
    initialize()
    run(host='localhost', port=8080, debug=True)


