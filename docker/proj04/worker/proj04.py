from flask import Flask, json, request
import collections
from flask.ext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
cuenta=0


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'VFhcs123!'
app.config['MYSQL_DATABASE_DB'] = 'fruit'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def hello():
    global cuenta
    cuenta=cuenta+1
    return "<h1 style='color:blue'>Hello There! v.012 c:"+str(cuenta)+"</h1>"


@app.route('/q1',methods=['POST','GET'])
def signUp():
    try:
        #_name = request.form['inputName']
        #_email = request.form['inputEmail']
        #_password = request.form['inputPassword']

        # validate the received values
        #if _name and _email and _password:
        #    return json.dumps({'html':'<span>Enter the required fields</span>'})

        # All Good, let's call MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""
                Select date,dc1,dc2
                From hDateDevices
                """)

        rows = cursor.fetchall()


        oList=[]
        for row in rows:
                d = collections.OrderedDict()
                d['date']=row[0].strftime("%Y-%m-%d")
                d['dc1']=row[1]
                d['dc2']=row[2]
                oList.append(d)

        return json.dumps(oList)


    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()


if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
