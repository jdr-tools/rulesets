from bson.objectid import ObjectId
from flask import jsonify, request
from ..models import Ruleset, Session
from .blueprints import rulesets_blueprint

@rulesets_blueprint.route('', methods = ['GET'])
def list() -> tuple:
  rulesets = []
  for ruleset in Ruleset.objects:
    rulesets.append({
      '_id': str(ruleset._id),
      'title': ruleset.title,
      'description': ruleset.description
    })
  return jsonify(rulesets)