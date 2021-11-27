 
# export FLASK_ENV=development
# export FLASK_APP="/home/shivasankaran/server/server.py"

# flask run --host=192.168.56.1 --cert=adhoc


from flask import Flask, redirect, url_for,send_from_directory,request
import flask
import sqlite3
from sqlite3 import Error
import ipinfo
import cachetools
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash





access_token = "ACCESS_TOKEN HERE"
app = Flask(__name__,static_url_path = '/home/mininet/pyscripts/server/assets/')
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin")
    
}
db_file = '/home/shivasankaran/server/assets/IP_data.db'
create_IPtable = """CREATE TABLE IF NOT EXISTS CLIENTDATA (
                                        Public_IP text NOT NULL,
                                        Private_IP text NOT NULL,
                                        Platform text NOT NULL,
                                        Browser text NOT NULL,
                                        Version text NOT NULL,
                                        INFO text NOT NULL,
                                        IP_INFO text NOT NULL,
                                        UNIQUE(Public_IP, Private_IP)

                                    )"""
def add_database(data):
    conn = None
    handler= ipinfo.getHandler(access_token,cache_options={'ttl':30, 'maxsize': 128})
    details = handler.getDetails(str(data[0]))
    ip_info = str(details.all)
    print("ip info:",ip_info)

    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute(create_IPtable)
        try:
          c.execute(""" INSERT INTO CLIENTDATA(Public_IP,Private_IP,Platform,Browser,Version,INFO,IP_INFO)
                VALUES(?,?,?,?,?,?,?)""",(data[0],data[1],data[2],data[3],data[4],data[5],ip_info))
        except:
          print("entry already present")
        c.execute("SELECT * FROM CLIENTDATA")
        print(c.fetchall())
        conn.commit()
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/admin')
@auth.login_required
def hello_admin():
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM CLIENTDATA")
        clients_data = c.fetchall()
        print(clients_data)
        print(type(clients_data))
        conn.close()

        return flask.render_template('table.html',test = clients_data)
    except Error as e:
        print(e)
        return "ERROR OPENING DATABASE"

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))

@app.route('/MyIP')
def getIP():
   print()
   return flask.render_template('home.html')

@app.route('/localIP',methods = ['POST'])
def localIP():
   if request.method == 'POST':
        public_IP = str(request.remote_addr)
        print(request.environ.get('REMOTE_PORT'))
        private_IP = str(request.data.decode())
        print("public IP :{} , private IP:{}".format(public_IP,private_IP))
        userinfo = request.user_agent
        data = [public_IP,private_IP, userinfo.platform,userinfo.browser,userinfo.version,userinfo.string]
        add_database(data)
        return public_IP
   return 'success'
if __name__ == '__main__':
   app.run(debug = True)
