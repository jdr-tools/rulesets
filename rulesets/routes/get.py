from flask import jsonify
from rulesets.models import Ruleset
from bson.objectid import ObjectId
from rulesets.routes.blueprints import rulesets_blueprint
from flask import g

@rulesets_blueprint.route("/<ruleset_id>", methods=['GET'])
def item(ruleset_id):
  return jsonify(
    title=g.ruleset.title,
    description=g.ruleset.description
  )