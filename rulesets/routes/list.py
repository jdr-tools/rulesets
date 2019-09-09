from flask import jsonify, request
from bson.objectid import ObjectId
from rulesets.models.ruleset import Ruleset
from rulesets.models.session import Session
from rulesets.routes.blueprints import rulesets_blueprint
import pdb

@rulesets_blueprint.route("", methods=['GET'])
def list():
  rulesets = []
  for ruleset in Ruleset.objects:
    rulesets.append({
      "_id": str(ruleset._id),
      "title": ruleset.title,
      "description": ruleset.description
    })
  return jsonify(rulesets)