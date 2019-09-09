from bson.objectid import ObjectId
from rulesets.models import Ruleset
from flask import jsonify
from rulesets.routes.blueprints import rulesets_blueprint
from flask import g

@rulesets_blueprint.route("/<ruleset_id>", methods=["DELETE"])
def delete(ruleset_id):
  g.ruleset.delete()
  return jsonify(message="deleted")