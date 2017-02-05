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
            Select distinct cust,count(*)
            From kpi
            group by cust
            order by cust
            """)

    #"""

    rows = cursor.fetchall()

    d = collections.OrderedDict()
    oList=[]
    for row in rows:
            d = collections.OrderedDict()
            d['cust']=row[0]
            d['count']=row[1]
            oList.append(d)


    return render_template('customerList.nj2', custs=oList)


@app.route('/customerDetail/<cust>')
def customerDetail(cust=None):

    # All Good, let's call MySQL
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("""
        Select cust,domain,
            ccmLoadAVG1_id,ccmLoadAVG1_value,
            ccmNtpStratum_id,ccmNtpStratum_value
        From hostStatus
            where cust=%s
            """,
            (cust))
    #"""
    oId=[]
    i = collections.OrderedDict()
    ####
    rows = cursor.fetchall()
    d = collections.OrderedDict()
    oList=[]
    for row in rows:
        d = collections.OrderedDict()
        d['cust']=row[0]
        d['domain']=row[1]
        d['ccmLoadAVG1_id']=row[2]
        d['ccmLoadAVG1_value']=row[3]
        d['ccmNtpStratum_id']=row[4]
        d['ccmNtpStratum_value']=row[5]
        oList.append(d)
        i = collections.OrderedDict()
        i['id']=row[2]
        oId.append(i)
        i = collections.OrderedDict()
        i['id']=row[4]
        oId.append(i)


    #Query 2: Perfmon
    cursor.execute("""
        Select cust,domain,
            RegisteredHardwarePhones_id,RegisteredHardwarePhones_value,
            CallsActive_id,CallsActive_value
        From perfmon
            where cust=%s
            """,
            (cust))
    #"""

    rows = cursor.fetchall()
    d = collections.OrderedDict()
    oList2=[]
    for row in rows:
        d = collections.OrderedDict()
        d['cust']=row[0]
        d['domain']=row[1]
        d['RegisteredHardwarePhones_id']=row[2]
        d['RegisteredHardwarePhones_value']=row[3]
        d['CallsActive_id']=row[4]
        d['CallsActive_value']=row[5]
        oList2.append(d)
        i = collections.OrderedDict()
        i['id']=row[2]
        oId.append(i)
        i = collections.OrderedDict()
        i['id']=row[4]
        oId.append(i)



    return render_template('customerDetail.nj2', cust=cust, kpis=oList, perfmon=oList2, kpisId=oId)





#Main
if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.debug=True
    app.run(host='0.0.0.0',port=8000)
