from flask import Flask, json, request, send_from_directory
from flask import render_template
import collections
from flask.ext.mysql import MySQL
import os
import logging
from logging.handlers import RotatingFileHandler

mysql = MySQL()
app = Flask(__name__)



cuenta=0

# MySQL configurations
#app.config['MYSQL_DATABASE_USER'] = os.environ.get('BDB_MYSQL_USER')
#app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('BDB_MYSQL_PASS')
#app.config['MYSQL_DATABASE_DB'] = os.environ.get('BDB_MYSQL_DB')
#app.config['MYSQL_DATABASE_HOST'] = os.environ.get('BDB_MYSQL_HOST')
#mysql.init_app(app)



# Dev paths
@app.route("/api/v1/q1")
def hello():
    global cuenta
    cuenta=cuenta+1
    return "<h1 style='color:blue'>Hello There! v.012 c:"+str(cuenta)+"</h1>"


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
    app.run(host='0.0.0.0', port=8012, debug=True)
