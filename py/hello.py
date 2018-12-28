# hello.py
from card import main
import json
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    path=environ['PATH_INFO'].split("=")[1]
    res = main(path)
    #return [type(environ).encode()]
    #return [str(environ).encode()]
    return [res.encode()]
