import logging
from flask import Flask
from flask import request,jsonify

from acelink_server.common import configure_loger
from acelink_server.docker_handler import run_acelink,del_container,get_container
from acelink_server.acestream_test import get_m3u8_age, get_status, list_streams
from acelink_server._version import __version__

app = Flask(__name__)


logger = logging.getLogger(__name__)



@app.route("/")
def hello_world():
    return {"result": "hi"}

@app.route("/hls/", methods=['GET'] )
def hls_list():

    result = list_streams()
    return result


@app.route("/hls/<int:port>/", methods=['GET','PUT','DELETE'] )
def hls_manager(port):

    result = {}

    code, msg = check_token(request)
    if code != 200:
        return jsonify(error=msg), code


    if request.method == 'GET':

        logger.info("query status for port:%d",port)
        config = get_container(port)

        status = get_status(port,config.get('ace_id'))
        m3u8_age = get_m3u8_age(port)

        result = { **config, **status }
        result['m3u8_age'] = m3u8_age

        logger.info("Status for port:%d description:%s, status:%s, m3u8 age:%s",
                    port,
                    config.get('description'),
                    status.get('status'),
                    m3u8_age)

        return result



    if request.method == 'DELETE':
        container_id = del_container(port)
        result={}
        result['result'] = 'ok'
        result['container_id'] = container_id
        return result

    if request.method == 'PUT':
        query = request.json 
        ace_id = query.get('ace_id')
        description = query.get('description')

        logger.info("new request, port:%d, ace_id:%s, description:%s",port,ace_id,description)

        container_id = None
        if port>=3000 and port <=3999:
            container_id = run_acelink(ace_id,port,description=description)

        result = query
        result['port'] = port
        result['result'] = 'ok'
        result['container_id'] = container_id

        return result


    return jsonify(error="Nothing to do"), 400



def check_token(request):
    """
    Demo security, dummy check
    """

    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return 403, "not authorization header"

    header = auth_header.split(' ')

    if len(header)!=2 or header[0] != "Bearer":
        return 403, "work authorization header format"

    token = header[1]

    if token != "MAGIC":
        return 403, "token not valid"

    return 200, "OK"



if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    logger.info("Starting acelinkd service, version %s",__version__)


if __name__ == '__main__':
    configure_loger()
    logger.info("Starting acelinkd service, version %s",__version__)
    app.run(host='127.0.0.1', port=5000, debug=True)
