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



@app.route('/customerList')
def customerlist(cust=None):

        # All Good, let's call MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""
                Select distinct cust
                From kpi
                Order by cust
                """)

        #"""

        rows = cursor.fetchall()

        d = collections.OrderedDict()
        oList=[]
        for row in rows:
                d = collections.OrderedDict()
                d['cust']=row[0]
                oList.append(d)


        return render_template('customerList.nj2', custs=oList)



@app.route('/customerDetail/<cust>')
def customerDetail(cust=None):

        # All Good, let's call MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""
                Select id,cust,kpi,domain
                From kpi
                where cust=%s and domain="/"
                """,
                (cust))
        #"""

        rows = cursor.fetchall()
        d = collections.OrderedDict()
        oList=[]
        for row in rows:
                d = collections.OrderedDict()
                d['id']=row[0]
                d['cust']=row[1]
                d['kpi']=row[2]
                d['domain']=row[3]
                oList.append(d)


        return render_template('customerDetail.nj2', cust=cust, kpis=oList)





#Main
if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.debug=True
    app.run(host='0.0.0.0',port=8000)
