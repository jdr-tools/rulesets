import os, sys, pdb, json

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from rulesets.models.account import Account
from rulesets.models.ruleset import Ruleset
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

import rulesets.routes.create
import rulesets.routes.list
import rulesets.routes.update
import rulesets.routes.get
import rulesets.routes.destroy