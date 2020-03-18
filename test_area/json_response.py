import os

import random, math
import requests, json
from flask import Flask, render_template, url_for, session, request, jsonify, make_response, redirect
from flask_session import Session

@app.route("/json", methods=["POST"])
def json2():

    if request.is_json:
        req = request.get_json()

        response = {
            "message": "JSON received",
            "name": req.get("name")
        }

        res = make_response(jsonify(response),200)

        return res
    else:
        res = make_response(jsonify({"message": "No JSON"}), 400)
        return res