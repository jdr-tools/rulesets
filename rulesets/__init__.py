import os, sys, json, pdb
from dotenv import load_dotenv
from flask import Flask, jsonify, request, g
from rulesets.models import Account, Ruleset, Session
from bson.objectid import ObjectId
from rulesets.routes.blueprints.rulesets import rulesets_blueprint
import rulesets.routes
from rulesets.helpers import api_error
from bson.errors import InvalidId

load_dotenv()
app = Flask(__name__, instance_relative_config=True)

@rulesets_blueprint.url_value_preprocessor
def pull_ruleset_id(endpoint, values):
  g.ruleset_id = values.get('ruleset_id', None)

@rulesets_blueprint.before_request
def add_body_to_params():
  if request.method in ['POST', 'PUT']:
    if request.json is not None:
      request.args = {**request.args, **request.json}

@rulesets_blueprint.before_request
def check_session():
  if 'session_id' not in request.args:
    return api_error(400, 'session_id.required')
  if request.args.get('session_id') == None:
    return api_error(400, 'session_id.required')
  sessions = Session.objects.raw({'token': request.args.get('session_id')})
  if sessions.count() == 0:
    return api_error(404, 'session_id.unknown')
  else:
    app.session = sessions[0]

@rulesets_blueprint.before_request
def check_ruleset():
  if g.ruleset_id != None:
    rulesets = Ruleset.objects.raw({"_id": ObjectId(g.ruleset_id)})
    if rulesets.count() == 0:
      return api_error(404, 'ruleset_id.unknown')
    else:
      g.ruleset = rulesets[0]

@rulesets_blueprint.before_request
def check_attributes():
  if request.endpoint in ['rulesets_blueprint.create', 'rulesets_blueprint.update']:
    # The missing title is only an error if creating the ruleset, you can not edit the title.
    if 'title' not in request.json:
      if request.endpoint == 'rulesets_blueprint.create':
        return api_error(400, 'title.required')
    elif len(request.json['title']) < 6:
      return api_error(400, 'title.too_short')

app.register_blueprint(rulesets_blueprint, url_prefix='/rulesets')

@app.errorhandler(InvalidId)
def handle_invalid_id(error):
  return api_error(404, 'ruleset_id.unknown')