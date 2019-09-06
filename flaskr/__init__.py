import os, sys, pdb, json

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flaskr.models.account import Account
from flaskr.models.ruleset import Ruleset
from bson.objectid import ObjectId

load_dotenv()
app = Flask(__name__, instance_relative_config=True)

@app.before_request
def check_session():
  try:
    ['GET', 'DELETE'].index(request.method)
  except ValueError:
    try:
      app.parsed_body = json.loads(request.data)
    except json.decoder.JSONDecodeError:
      app.parsed_body = {}

import flaskr.routes.create
import flaskr.routes.list
import flaskr.routes.update
import flaskr.routes.get
import flaskr.routes.destroy