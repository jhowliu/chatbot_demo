#!flask/bin/python
from app import app
app.run(host='192.168.10.16', debug=True, threaded=True)
