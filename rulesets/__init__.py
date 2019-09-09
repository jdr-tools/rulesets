import os, sys, pdb, json
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from rulesets.models.account import Account
from rulesets.models.ruleset import Ruleset
from rulesets.models.session import Session
from bson.objectid import ObjectId
from rulesets.routes.blueprints.rulesets import rulesets_blueprint
import rulesets.routes

load_dotenv()
app = Flask(__name__, instance_relative_config=True)

@rulesets_blueprint.before_request
def add_body_to_params():
  if request.method in ['POST', 'PUT']:
    if request.json is not None:
      request.args = {**request.args, **request.json}

@rulesets_blueprint.before_request
def check_session():
  if 'session_id' not in request.args:
    return jsonify({'message': 'session_id_required'}), 400
  if request.args.get('session_id') == None:
    return jsonify({'message': 'session_id_required'}), 400
  sessions = Session.objects.raw({'token': request.args.get('session_id')})
  if sessions.count() == 0:
    return jsonify({'message': 'session_id_unknown'}), 404

app.register_blueprint(rulesets_blueprint, url_prefix='/rulesets')