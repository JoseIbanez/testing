from flask import Flask
application = Flask(__name__)
cuenta=0

@application.route("/")
def hello():
    global cuenta
    cuenta=cuenta+1
    return "<h1 style='color:blue'>Hello There! c:"+str(cuenta)+"</h1>"

if __name__ == "__main__":
    application.run(host='0.0.0.0')
