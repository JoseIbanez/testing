from flask import Flask, json, request, send_from_directory
import collections
from flask.ext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__,static_url_path='')
cuenta=0

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'VFhcs123!'
app.config['MYSQL_DATABASE_DB'] = 'fruit'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#Static Files
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/')
def root():
    return app.send_static_file('./static/index.html')


# Dev paths

@app.route("/q2")
def hello():
    global cuenta
    cuenta=cuenta+1
    return "<h1 style='color:blue'>Hello There! v.012 c:"+str(cuenta)+"</h1>"


@app.route('/kpi',methods=['POST','GET'])
def signUp():
    try:
        #_name = request.form['inputName']
        #_email = request.form['inputEmail']
        #_password = request.form['inputPassword']

        # validate the received values
        #if _name and _email and _password:
        #    return json.dumps({'html':'<span>Enter the required fields</span>'})


        cust   = request.form['cust']
        kpi    = request.form['kpi']
        domain = request.form['domain']

        if cust and kpi and domain:
            return json.dumps({'html':'<span>Enter the required fields</span>'})


        # All Good, let's call MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""
                Select date,value
                From kpi
                where cust=% and kpi=% and domain=%
                """,
		cust,kpi,domain)

        rows = cursor.fetchall()


        oList=[]
        for row in rows:
                d = collections.OrderedDict()
                d['date']=row[0].strftime("%Y-%m-%d %H:%M")
                d['value']=row[1]
                oList.append(d)

        #return json.dumps(oList)
        return json.dumps(d)


    except Exception as e:
        return json.dumps({'error':str(e)})

    finally:
        cursor.close() 
        conn.close()


if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
