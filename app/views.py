from flask import render_template, request, redirect, session
from app.model import get_result_with_text, id_generator
from app import app

session_id = ""

@app.route('/')
@app.route('/index')
def home():
    session['id'] = id_generator(size=12)
    print "new session = {}".format(session['id'])
    return render_template('index.html',
                           title='chatbot demo')

@app.route('/test', methods=['GET'])
def test():
    session_id = session['id']
    raw_text = request.args.get('text')
    print "client with {}".format(session_id)
    json_object = get_result_with_text(raw_text, session_id)

    return json_object 

@app.route('/foo', methods=['POST'])
def foo():
    session_id = session['id']
    raw_text = request.form['raw_text']
    print "client with {}".format(session_id)
    json_object = get_result_with_text(raw_text, session_id)

    return json_object

app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
