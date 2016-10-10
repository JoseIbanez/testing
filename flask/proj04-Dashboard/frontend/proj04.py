from flask import Flask, json, request, send_from_directory
from flask import render_template
import collections
from flask.ext.mysql import MySQL
#from flask.mysql import MySQL

import logging
from logging.handlers import RotatingFileHandler

mysql = MySQL()
#app = Flask(__name__,static_url_path='')
app = Flask(__name__)

cuenta=0

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'VFhcs123!'
app.config['MYSQL_DATABASE_DB'] = 'fruit'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#Static Files
@app.route('/data/<path:path>')
def send_data(path):
    return send_from_directory('data', path)

@app.route('/dist/<path:path>')
def send_dist(path):
    return send_from_directory('dist', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/pages/<path:path>')
def send_pages(path):
    return send_from_directory('pages', path)

@app.route('/vendor/<path:path>')
def send_vendor(path):
    return send_from_directory('vendor', path)

@app.route('/')
def send_index():
    return render_template('index.html')

# Render templates

@app.route('/perfmon/')
@app.route('/perfmon/<cust>')
def perfmon(cust=None):

        kpi="RegisteredPhones"
        domain="/UK%"

        # All Good, let's call MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""
                Select id,domain,value
                From kpi
                where cust=%s and kpi=%s and domain like %s
                order by domain
                """,
                (cust,kpi,domain))
        #"""

        rows = cursor.fetchall()

        d = collections.OrderedDict()
        oList=[]
        for row in rows:
                d = collections.OrderedDict()
                d['id']=row[0]
                d['domain']=row[1]
                d['value']=row[2]
                oList.append(d)


        return render_template('perfmon.nj2', cust=cust, domains=oList)

# Dev paths

@app.route("/q1")
def hello():
    global cuenta
    cuenta=cuenta+1
    return "<h1 style='color:blue'>Hello There! v.012 c:"+str(cuenta)+"</h1>"

@app.route("/q2")
def kpi2():
    global cuenta
    cuenta=cuenta+1
    data={"kpi1":cuenta, 
	  "kpi2":2000}
    return json.dumps(data) 

#############3
# KPI
#

#
# Single value
#
@app.route('/kpi',methods=['POST','GET'])
def getKpi():
    try:

        app.logger.info('Info')

        cust="Cust16"
        kpi="RegisteredPhones"
        domain="/"
        cust   = request.values.get('cust')
        kpi    = request.values.get('kpi')
        domain = request.values.get('domain')

        app.logger.info('Info: cust'+cust+', kpi:'+kpi+', domain:'+domain)


        if not (cust and kpi and domain):
            return json.dumps({'html':'<span>Enter the required fields</span>'})


        # All Good, let's call MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""
                Select date,value
                From kpi
                where cust=%s and kpi=%s and domain=%s
                """,
		(cust,kpi,domain))
        #"""
        rows = cursor.fetchall()

        d = collections.OrderedDict()
        oList=[]
        for row in rows:
                d = collections.OrderedDict()
                d['date']=row[0].strftime("%Y-%m-%d %H:%M:%SZ")
                d['value']=row[1]
                oList.append(d)


        #return json.dumps(oList)
        return json.dumps(d)


    except Exception as e:
        return json.dumps({'error':str(e)})

    finally:
        cursor.close()
        conn.close()

#
#like format
#
@app.route('/list',methods=['POST','GET'])
def getList():
    try:

        app.logger.info('Info')

        cust="Cust16"
        kpi="RegisteredPhones"
        domain="/"
        cust   = request.values.get('cust')
        kpi    = request.values.get('kpi')
        domain = request.values.get('domain')+'%'

        app.logger.info('Info: cust'+cust+', kpi:'+kpi+', domain:'+domain)


        if not (cust and kpi and domain):
            return json.dumps({'html':'<span>Enter the required fields</span>'})


        # All Good, let's call MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""
                Select id,date,value,domain
                From kpi
                where cust=%s and kpi=%s and domain like %s
                """,
                (cust,kpi,domain))
        #"""
        rows = cursor.fetchall()


        oList=[]
        for row in rows:
                d = collections.OrderedDict()
                d['id']=row[0]
                d['date']=row[1].strftime("%Y-%m-%d %H:%M")
                d['value']=row[2]
                d['domain']=row[3]
                oList.append(d)


        return json.dumps(oList)
        #return json.dumps(d)


    except Exception as e:
        return json.dumps({'error':str(e)})

    finally:
        cursor.close()

#
#Log format
#
@app.route('/log',methods=['POST','GET'])
def getLog():
    try:

        app.logger.info('Info')

        cust="Cust16"
        kpi="RegisteredPhones"
        domain="/"
        cust   = request.values.get('cust')
        kpi    = request.values.get('kpi')
        domain = request.values.get('domain')

        app.logger.info('Info: cust'+cust+', kpi:'+kpi+', domain:'+domain)


        if not (cust and kpi and domain):
            return json.dumps({'html':'<span>Enter the required fields</span>'})


        # All Good, let's call MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""
                Select * from (
                  select date,value 
                  from log 
                  where cust=%s and kpi=%s and domain=%s
                  order by date desc 
                  limit 5
                ) sub 
                order by date;
                """,
                (cust,kpi,domain))
        #"""
        rows = cursor.fetchall()

        d = collections.OrderedDict()
        oList=[]
        for row in rows:
                d = collections.OrderedDict()
                d['date']=row[0].strftime("%Y-%m-%d %H:%M:%SZ")
                d['value']=row[1]
                oList.append(d)

        return json.dumps(oList)


    except Exception as e:
        return json.dumps({'error':str(e)})

    finally:
        cursor.close()
        conn.close()







#Main

if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.debug=True
    app.run(host='0.0.0.0')
