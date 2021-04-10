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

#USERS
#--------------------------------------------------------------
@route('/add-user', method='POST')
#adds a new usre to the users sql 
def do_add_user():
    l_username = request.forms.get('username')
    l_pwd = request.forms.get('password')
    l_id = 12 #TODO: add later

    conn = sqlite3.connect('masking.db')
    c = conn.cursor()
    c.execute("INSERT INTO users(ID, NAME, PASSWORD) VALUES(?, ?, ?)", (l_id, l_username, l_pwd))
    print("user " + l_username + " was added succesfully")
    conn.commit()
    conn.close()
    return template('op-succes.tpl', op_name = "add user")


@route('/delete-user', method = 'POST')
# function deletes a user from databace
def do_delete_user():
    l_name = request.forms.get('username')
    print("username: " + l_name)
    conn = sqlite3.connect('masking.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE name=?", (l_name,))
    conn.commit()
    return template('op-succes.tpl', op_name = "delete user")

#--------------------------------------------------------------

#SENSORS
#--------------------------------------------------------------
@route('/sensors', method = "post")
def do_sensors_menu():
    if request.forms.get('bt1') == "Add Sensor" :
        return template('add-user.tpl')
    elif request.forms.get('bt2') == "Delete Sensor" :
        return template('delete-user.tpl')
    elif request.forms.get('bt3') == "Show All Sensor" :
        conn = sqlite3.connect('masking.db')
        c = conn.cursor()
        c.execute("SELECT * FROM sensors")
        rows = c.fetchall()
        for row in rows:
            print(row[1])
        return template('show-all-users.tpl', tpl_rows = rows)
    elif request.forms.get('bt4') == "Back" :
        return template('main.tpl')
    else:
        print("Wrong selection")

@route('/add-sensor', method='POST')
#adds a new usre to the users sql 
def do_add_sensor():
    l_UUID = request.forms.get('UUID')
    l_pwd = request.forms.get('password')

    conn = sqlite3.connect('masking.db')
    c = conn.cursor()
    #c.execute("INSERT INTO sensors(UUID, PASSWORD) VALUES(?, ?)", (l_UUID l_pwd))
    print("sensor " + l_UUID + " was added succesfully")
    conn.commit()
    conn.close()
    return template('op-succes.tpl', op_name = "add sensor")

@route('/delete-sensor', method = 'POST')
# function deletes a sensor from databace
def do_delete_sensor():
    l_UUID = request.forms.get('UUID')
    print("UUID: " + l_UUID)
    conn = sqlite3.connect('masking.db')
    c = conn.cursor()
    c.execute("DELETE FROM sensors WHERE UUID=?", (l_UUID,))
    conn.commit()
    return template('op-succes.tpl', op_name = "delete sensor")
#-----------------------------------------------------

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
##
@route('/users', method = "post")
# function that sends us from users template 
# to other avaible themplates
def do_users_menu():
    if request.forms.get('bt1') == "Add User" :
        return template('add-user.tpl', usr_id=222)
    elif request.forms.get('bt2') == "Delete User" :
        print("reached delete user")
        return template('delete-user.tpl',  usr_id=222)
    elif request.forms.get('bt3') == "Show All Users" :
        conn = sqlite3.connect('masking.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        for row in rows:
            print(row[1])
        return template('show-all-users.tpl', tpl_rows = rows)
    elif request.forms.get('bt4') == "Back" :
        return template('main.tpl')
    else:
        print("Wrong selection")

@route('/user-added', method = "post")
# function that takes us back to the main menu from user-added
def do_added_menu():
    if request.forms.get('bt1') == "Back" :
        return template('main.tpl')

@route('/show-all-users', method = "post")
# function that takes us back to the main menu from show-all-users
def show(): 
    if request.forms.get('bt1') == "Back" :
        return template('main.tpl')

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

# add to sql request in main
# to add a table to this page
@route('/sql-request', method='POST')
def do_sql_request():
    sql_query = request.forms.get('sql-query')
    conn = sqlite3.connect('masking.db')
    c = conn.cursor()
    c.execute(sql_query)
    rows = c.fetchall()
    
    for row in rows:
        for el in row:
            if type(el) == int:
                el = str(el)
            print(el + " "),
        print("")

    return template('show-sql-request.tpl', sql_request=sql_query, tpl_rows=rows)

def initialize():
    if os.path.isfile('masking.db'):
        print("the database already exists")
    else:
        print("creating the database")
        conn = sqlite3.connect('masking.db')
        c = conn.cursor()
        c.execute("CREATE TABLE raw_data(id TEXT, date TEXT, status TEXT)")
        c.execute("CREATE TABLE users(id TEXT, name TEXT, password TEXT)")
        c.execute("CREATE TABLE sensors(UUID TEXT, password TEXT)")

        conn.close() 

    #יוצרת DB במידה והאו לא קיים



if __name__ == '__main__':
    initialize()
    run(host='localhost', port=8080, debug=True)


