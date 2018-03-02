# -*- coding=utf-8 -*-
from flask import render_template, request, session, jsonify
from app.model import get_result_with_text, id_generator, initial
from app import app

import json

session_id = ""


@app.route('/')
@app.route('/index')
def home():
    session['id'] = id_generator(size=12)
    print "new session = {}".format(session['id'])
    return render_template('index.html',
                           title='chatbot demo')


@app.route('/<app_id>/setting')
def setting(app_id):
    if 'id' not in session:
        return "Not Found"

    return render_template('settings.html', title='Setting')


@app.route('/<app_id>')
def chatbot(app_id):
    session['id'] = id_generator(size=20)
    session['app_id'] = app_id
    print "new session = {}".format(session['id'])
    print "new app_id = {}".format(session['app_id'])

    return render_template('chatbot.html', title='LingBot')


@app.route('/<app_id>/<id_no>/<user>/<service_type>/<date>')
def demo(app_id, id_no, user, service_type, date):
    session['app_id'] = app_id
    session['user'] = user
    session['id_no'] = id_no
    session['date'] = date
    session['id'] = id_generator(size=20)
    session['service_type'] = service_type

    return render_template('chatbot.html', title='Demo')


@app.route('/test', methods=['GET'])
def test():
    session_id = session['id']
    raw_text = request.args.get('text')
    print "client with {}".format(session_id)
    json_object, audio_file_name = get_result_with_text(raw_text, session_id)

    return json_object


@app.route('/init', methods=['POST'])
def init():
    app_id = session['app_id']

    if app_id != "sunshine":
        return json.dumps({"dialogueReply": None})

    user = session['user']
    date = session['date']
    id_no = session['id_no']
    session_id = session['id']
    service_type = session['service_type']

    json_object = initial(session_id, app_id, id_no, user, service_type, date)

    return json_object


@app.route('/foo', methods=['POST'])
def foo():
    app_id = session['app_id']
    session_id = session['id']
    raw_text = request.form['raw_text']

    print "client with {}".format(session_id)

    json_object, audio_file_name = \
        get_result_with_text(raw_text, session_id, app_id)
    json_object = json.loads(json_object)
    json_object['audio_file_name'] = audio_file_name

    return jsonify(json_object)


# store their id and session_id
sender_list = {}


@app.route('/fb-bot', methods=['POST'])
def fb():
    global sender_list

    sender_id = request.form['sender_id']
    raw_text = request.form['raw_text']

    print sender_id, raw_text
    print sender_list

    if sender_id not in sender_list:
        sender_list[sender_id] = id_generator(size=20)

    session_id = sender_list[sender_id]

    json_text = get_result_with_text(raw_text, session_id, 'renda')

    json_object = json.loads(json_text)

    if raw_text == u'重新' or raw_text.lower() == 'reset':
        print "reset the session id"
        sender_list[sender_id] = id_generator(size=20) # reset the session_id
        return "session_reset"

    # create new session_id if finished the dialogue
    if json_object['dialogue_state'] == 'completed':
        sender_list[sender_id] = id_generator(size=20) # reset the session_id

        # get schedule when task is done if request schedule info. (need talk claude change his flow)
        if 'task' in json_object and json_object['task']['TaskName'] == 'HSRScheduleInfo':
            _, url = get_schedule_with_data(json.dumps(json_object['task']), session_id)
            json_object['dialogueReply'] = url
            return json.dumps(json_object)

    return json_text


@app.route('/get_schedule', methods=['POST'])
def get_schedule():
    session_id = session['id']
    post_data = request.form['data']

    response, _ = get_schedule_with_data(post_data, session_id)
    print(response)
    #return ('None', 200) if response is None else response
    return json.dumps(response) # return the json object



app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
