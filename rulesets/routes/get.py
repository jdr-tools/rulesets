from bson.objectid import ObjectId
from flask import jsonify, g
from ..models import Ruleset
from .blueprints import rulesets_blueprint

@rulesets_blueprint.route('/<ruleset_id>', methods=['GET'])
def item(ruleset_id):
  return jsonify(
    title = g.ruleset.title,
    description = g.ruleset.description
  )