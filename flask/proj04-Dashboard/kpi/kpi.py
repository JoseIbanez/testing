from flask import Flask, json, request, send_from_directory
from flask import render_template
import collections
from flask.ext.mysql import MySQL
#from flask.mysql import MySQL
import os
import logging
from logging.handlers import RotatingFileHandler

mysql = MySQL()
#app = Flask(__name__,static_url_path='')
app = Flask(__name__)



cuenta=0

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.environ.get('BDB_MYSQL_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('BDB_MYSQL_PASS')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('BDB_MYSQL_DB')
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('BDB_MYSQL_HOST')
mysql.init_app(app)



# Dev paths
@app.route("/api/v1/q1")
def hello():
    global cuenta
    cuenta=cuenta+1
    return "<h1 style='color:blue'>Hello There! v.012 c:"+str(cuenta)+"</h1>"

@app.route("/api/v1/q2")
def kpi2():
    global cuenta
    cuenta=cuenta+1
    data={"kpi1":cuenta,
	  "kpi2":2000}
    return json.dumps(data)

@app.before_first_request
def testDB():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

    app.logger.info('Info>>Testing logger')
    app.logger.error('Error>>Testing logger')
    app.logger.info('Testing DB connection')

    try:
        # All Good, let's call MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""
                Select count(*)
                From kpi
                """)
        #"""
        rows = cursor.fetchall()
        for row in rows:
            count=row[0]
            app.logger.info('Count kpi table: '+count)

        cursor.close()
        conn.close()
        return 0

    except Exception as e:
        app.logger.info('DB connection error '+str(e))
        return -1


#############3
# KPI
#

#
# Single value
#
@app.route('/api/v1/kpi',methods=['POST','GET'])
def getKpi():

    app.logger.info('New KPI request')

    cust   = request.values.get('cust')
    kpi    = request.values.get('kpi')
    domain = request.values.get('domain')

    if not (cust and kpi and domain):
        return json.dumps({'html':'<span>Enter the required fields</span>'})

    app.logger.info('Info: cust'+cust+', kpi:'+kpi+', domain:'+domain)


    try:
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

        cursor.close()
        conn.close()
        #return json.dumps(oList)
        return json.dumps(d)


    except Exception as e:
        return json.dumps({'error':str(e)})

#
#like format
#
@app.route('/api/v1/list',methods=['POST','GET'])
def getList():
    try:

        app.logger.info('Info')

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
@app.route('/api/v1/log',methods=['POST','GET'])
def getLog():
    try:

        app.logger.info('New request: LOG')

        cust   = request.values.get('cust')
        kpi    = request.values.get('kpi')
        domain = request.values.get('domain')

        app.logger.info('Input: cust:'+cust+', kpi:'+kpi+', domain:'+domain)


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
                  limit 60
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
    #handler = RotatingFileHandler('/tmp/foo.log', maxBytes=10000, backupCount=1)
    #handler.setLevel(logging.DEBUG)
    #app.logger.addHandler(handler)
    #app.logger.setLevel(logging.DEBUG)
    #app.logger.handlers.extend(logging.getLogger("gunicorn.error").handlers)

    #handler = logging.StreamHandler()
    #handler.setLevel(logging.INFO)
    #app.logger.addHandler(handler)
    #app.logger.setLevel(logging.INFO)
    # fix gives access to the gunicorn error log facility
    #app.logger.handlers.extend(logging.getLogger("gunicorn.error").handlers)
    #app.debug=True
    app.run(host='0.0.0.0')
