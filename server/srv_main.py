# This Python file uses the following encoding: utf-8
from bottle import run, get, post, request, delete, route, template, static_file
import sqlite3
import os.path
import random
import glob

# Globals
g_bkp_dir = '.' # TODO: get the backup dir from running environment
 



#to write a route for login

# STATIC DATA
@get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    print("[DEBUG]: ", filepath)
    return static_file(filepath, root="../static/img")

#------------------------
# SENSOR related routes
#------------------------
@post('/connect_sensor')
def connect_sensor():
    sensor_ask = request.json.get('sensor_uuid')
    print(sensor_ask)
    return "Connect sensor - OK"

@post('/send_buffer')
def accept_data():
    print("send_buffer: accepted")
    buffer = request.json['buffer']
    conn = sqlite3.connect('masking.db')
    #c = cursor
    c = conn.cursor()
    for block in buffer:
        id = block['id']
        date = block['date']
        status = block['status']
        print("send_buffer: " , id, ", ", date, ", ", status)
        c.execute("INSERT INTO raw_data(ID, DATE, STATUS) VALUES(?, ?, ?)", (id, date, status))
        conn.commit()
    conn.close()

# LOGIN
#--------------------------------------------------------------
@route('/login')
def login():
    print("entering login route")
    return template('login.tpl')
#--------------------------------------------------------------

@route('/login', method = "post")
def do_login():
    if request.forms.get('bt1') == "Users" :
        return template('users.tpl')
    

# MAIN
#--------------------------------------------------------------
@route('/main')
def main_menu():
    print("entering main route")
    return template('main.tpl')
#--------------------------------------------------------------

@route('/main', method = "post")
def do_main_menu():
    if request.forms.get('bt1') == "Users" :
        return template('users.tpl')
    if request.forms.get('bt2') == "Sensors" :
        return template('sensors.tpl')
    if request.forms.get('bt3') == "SQL Request" :
        return template('sql-request.tpl')
    if request.forms.get('bt4') == "DB Opse" :
        return template('db-opse.tpl')
#--------------------------------------------------------------


#USERS
#--------------------------------------------------------------
@route('/users', method = "post")
# function that sends us from users template 
# to other avaible themplates
def do_users_menu():
    if request.forms.get('bt1') == "Add User" :
        return template('add-user.tpl', usr_id=222)
    elif request.forms.get('bt2') == "Delete User" :
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
#-----------------------------------------------------

@route('/add-user', method='POST')
#adds a new usre to the users sql 
def do_add_user():
    if request.forms.get('bt1') == "Back" :
            return template('users.tpl')

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
#-----------------------------------------------------

@route('/delete-user', method = 'POST')
# function deletes a user from databace
def do_delete_user():
    if request.forms.get('bt1') == "Back" :
            return template('users.tpl')

    l_name = request.forms.get('username')
    print("username: " + l_name)
    conn = sqlite3.connect('masking.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE name=?", (l_name,))
    conn.commit()
    return template('op-succes.tpl', op_name = "delete user")
#--------------------------------------------------------------

@route('/show-all-users', method = "post")
# function that takes us back to the main menu from show-all-users
def show(): 
    if request.forms.get('bt1') == "Back" :
        return template('users.tpl')
#--------------------------------------------------------------

#SENSORS
#--------------------------------------------------------------
@route('/sensors', method = "post")
def do_sensors_menu():
    if request.forms.get('bt1') == "Add Sensor" :
        return template('add-sensor.tpl')
    elif request.forms.get('bt2') == "Delete Sensor" :
        return template('delete-sensor.tpl')
    elif request.forms.get('bt3') == "Show All Sensors" :
        conn = sqlite3.connect('masking.db')
        c = conn.cursor()
        c.execute("SELECT * FROM sensors")
        rows = c.fetchall()
        for row in rows:
            print(row[1])
        return template('show-all-sensors.tpl', tpl_rows = rows)
    elif request.forms.get('bt4') == "Back" :
        return template('main.tpl')
    else:
        print("Wrong selection")
#-----------------------------------------------------

@route('/add-sensor', method='POST')
#adds a new usre to the users sql 
def do_add_sensor():
    if request.forms.get('bt1') == "Back" :
            return template('sensors.tpl')

    l_UUID = request.forms.get('uuid')
    l_pwd = request.forms.get('password')
    print (l_UUID, " ", l_pwd)
    conn = sqlite3.connect('masking.db')
    c = conn.cursor()
    c.execute("INSERT INTO sensors(UUID, PASSWORD) VALUES(?, ?)", (l_UUID, l_pwd))
    print("sensor ", l_UUID, " was added succesfully")
    conn.commit()
    conn.close()
    return template('op-succes.tpl', op_name = "add sensor")
#-----------------------------------------------------

@route('/delete-sensor', method = 'POST')
# function deletes a sensor from databace
def do_delete_sensor():
    if request.forms.get('bt1') == "Back" :
            return template('sensors.tpl')

    l_UUID = request.forms.get('uuid')
    print("uuid: " + l_UUID)
    conn = sqlite3.connect('masking.db')
    c = conn.cursor()
    c.execute("DELETE FROM sensors WHERE uuid=?", (l_UUID,))
    conn.commit()
    return template('op-succes.tpl', op_name = "delete sensor")
#-----------------------------------------------------

@route('/show-all-sensors', method = "post")
# function that takes us back to the main menu from show-all-users
def show(): 
    if request.forms.get('bt1') == "Back" :
        return template('main.tpl')
#-----------------------------------------------------



@route('/user-added', method = "post")
# function that takes us back to the main menu from user-added
def do_added_menu():
    if request.forms.get('bt1') == "Back" :
        return template('main.tpl')


@get('/test')
def test():
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

#SQL REQUEST
#--------------------------------------------------------------
# add to sql request in main
# to add a table to this page
@route('/sql-request', method='POST')
def do_sql_request():
    if request.forms.get('bt1') == "Back" :
                return template('main.tpl')

    print("debug: do_sql_request reached")
    sql_query = request.forms.get('sql-query')
    print("Query: ", sql_query)
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
#--------------------------------------------------------------


#--------
# DB OPS
#--------
@route('/dbops', method = "post")
def do_dbops_menu():
    if request.forms.get('bt1') == "Backup DB" :
        return template('bkp-db.tpl')
    elif request.forms.get('bt2') == "Restore DB" :
        return template('rst-db.tpl')
    elif request.forms.get('bt3') == "Purge Table" :
        return template('prg-tbl.tpl')
    elif request.forms.get('bt5') == "File List" :
        # create list of DB backup files
        bkp_files_path = os.path.join(g_bkp_dir, '*.dbkp')
        bkp_files_list = glob.glob(bkp_files_path)
        print("[DEBUG] backup files list: ", bkp_files_list)
        return template('table-list.tpl', lst_header = "DB backup files list", lst_data = bkp_files_list)
    elif request.forms.get('bt4') == "Back" :
        return template('main.tpl')
    else:
        print("[DEBUG] DB Ops - wrong selection")

@route('/bkp-db', method='POST')
def do_bkp_db():
    if request.forms.get('bt1') == "Back" :
        return template('db-opse.tpl')
        
    l_filename = request.forms.get('name') + ".dbkp"
    print("[DEBUG] backup file name: ", l_filename)
    con = sqlite3.connect('masking.db')
    bkp = sqlite3.connect(l_filename)
    with bkp:
        con.backup(bkp, pages=1, progress=progress)
    bkp.close()
    con.close()
    return template('op-succes.tpl', op_name = "backup db")

def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')
    
@route('/rst-db', method='POST')
def do_rst_db():
    """ Reset DB handler """
    if request.forms.get('bt1') == "Back" :
        return template('db-opse.tpl')
    
    l_restore_db_name = request.forms.get('file_name') + ".dbkp"
    
    # reading backup db in memory, close it 
    # and then write it back to original file
    src = sqlite3.connect(l_restore_db_name)
    mem = sqlite3.connect(':memory:')
    src.backup(dst)
    src.close()
    dst = sqlite3.connect('masking.db')
    with dst:
        mem.backup(dst, pages=1, progress=progress)
    dst.close()
    mem.close()
    
        
@route('/prg-tbl', method='POST')
def do_prg_tbl():
    """ Purge Table handler """
    if request.forms.get('bt1') == "Back" :
        return template('db-opse.tpl')
    
    l_tbl_name = request.forms.get('tbl_name')
    l_drop_cmd = "DELETE FROM " + l_tbl_name + ";" 
    
    print("[DEBUG] drop the table " + l_tbl_name + "with the command \"" + l_drop_cmd + "\"")
    
    con = sqlite3.connect('masking.db')
    c = con.cursor()
    c.execute(l_drop_cmd,)
    con.commit()
    con.close()
    l_op_name = "delete all data from table " + l_tbl_name
    return template('op-succes.tpl', op_name = l_op_name)


def initialize():
    if os.path.isfile('masking.db'):
        print("the database already exists")
    else:
        print("creating the database")
        conn = sqlite3.connect('masking.db')
        c = conn.cursor()
        c.execute("CREATE TABLE raw_data(id TEXT, date TEXT, status TEXT)")
        c.execute("CREATE TABLE users(id TEXT, name TEXT, password TEXT)")
        c.execute("CREATE TABLE sensors(uuid TEXT, password TEXT)")

        conn.close() 
    #יוצרת DB במידה והאו לא קיים



if __name__ == '__main__':
    initialize()
    run(host='localhost', port=8080, debug=True)


