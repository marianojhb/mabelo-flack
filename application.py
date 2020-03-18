import os

from datetime import datetime
import random, math
import requests, json
from flask import Flask, render_template, url_for, session, request, jsonify, make_response, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
# app.run(host= '0.0.0.0')

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET","POST"])
def index():
    session["title"] = "Project 2: Flack | Home"
    return render_template("index.html",session=session)

@app.route("/login", methods=["POST"])
def login():
    session["displayname"] = request.form.get("displayname")
    displayname = session["displayname"]
    res = make_response(jsonify({"success": True, "displayname": displayname}),200)
    return res

@app.route('/logout')
def logout():
    session.pop("displayname", None)
    return redirect('/')

@app.route('/channels',methods=["GET","POST"])
def channels():
    session["title"] = "Project 2: Flack | Channels"

    # # Load current 
    try:
        with open('static/channels.json') as json_file:
            session['data'] = json.load(json_file) # data is a json object
    except FileNotFoundError:
            print("File not accessible")
    return render_template("channels.html",session=session)

@app.route("/retrievechannels",methods=["POST"])
def retrievechannels():

    # Function to randomly add a color to new channel
    def channelcolor():
        channelcolors = ['badge-primary', 'badge-secondary', 'badge-success', 'badge-danger', 'badge-warning', 'badge-info', 'badge-light', 'badge-dark']
        color = channelcolors [ math.floor( random.random() * len(channelcolors) ) ]
        return color

    # Get name of channel from channels.html
    newchannel = request.form.get("channelname")

    # Check for existing channel
    addchannel = True
    for e in session['data']['channels']:
        if newchannel in e['channel']:
            addchannel = False
    if addchannel == True:

        # Create new channel after verifying new channel don't exist previously
        session['data']["channels"].append({"channel" : newchannel, "owner": session["displayname"], "color": channelcolor(), "messages" : [] })
        
        # Sort channels alphabetically:
        session['data']["channels"] = sorted(session['data']["channels"], key=lambda k: k['channel'])

    # Write new channellist to disk
    json_string = json.dumps(session['data'])
    with open('static/channels.json','w') as f:
        f.write(json_string)
        f.close()

    res = make_response(jsonify({"success": True, "data": session['data'] }),200)
    return res

@app.route("/channels/<string:channel>",methods=["GET","POST"])
def channel(channel):
    session["channel"] = channel
    return render_template("channel.html",session=session) 


@app.route("/messages")
def messages():
    session["title"] = "Project 2: Flack | Messages"
    return render_template("messages.html",session=session)

@app.route("/about")
def about():
    session["title"] = "Project 2: Flack | About"
    return render_template("about.html",session=session)

@socketio.on("submit message")
def message(data):
    print(data);
    message = data["message"]
    displayname = session['displayname']
    timestamp = datetime.now().strftime('%d/%m/%y %H:%M:%S')

    try:
        with open('static/channels.json') as json_file:
            session['data'] = json.load(json_file) # data is a json object
    except FileNotFoundError:
            print("File not accessible")
         
    # Save chat to json
    for item in session["data"]["channels"] :
        if item['channel'] == session['channel']:
            item["messages"].append({"sender" : displayname, "date" :  timestamp, "message" : message })
 
    json_string = json.dumps(session['data'])
    with open('static/channels.json','w') as f:
        f.write(json_string)
        f.close()

    emit("announce message", {"displayname": displayname, "timestamp": timestamp, "message": message}, broadcast=True)

