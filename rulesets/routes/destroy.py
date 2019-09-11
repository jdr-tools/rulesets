from bson.objectid import ObjectId
from flask import jsonify, g
from ..models import Ruleset
from .blueprints import rulesets_blueprint

@rulesets_blueprint.route('/<ruleset_id>', methods = ["DELETE"])
def delete(ruleset_id):
  g.ruleset.delete()
  return jsonify(message = 'deleted')