from flask import render_template, request, redirect
from app.model import get_result_with_text
from app import app

@app.route('/')
@app.route('/index')
def home():
    user = {'nickname': 'jhow'}
    return render_template('index.html',
                           title='chatbot demo',
                           user=user)

@app.route('/foo', methods=['POST'])
def foo():

    session_id = "aasdadasjli19999118188"
    raw_text = request.form['raw_text']
    json_object = get_result_with_text(raw_text, session_id)

    return json_object