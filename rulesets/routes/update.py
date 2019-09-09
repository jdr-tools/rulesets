from rulesets.models.ruleset import Ruleset
from flask import jsonify, request
from bson.objectid import ObjectId
from rulesets.routes.blueprints import rulesets_blueprint
from flask import g

@rulesets_blueprint.route("/<ruleset_id>", methods=['PUT'])
def update(ruleset_id):

  if 'title' in request.json:
    g.ruleset.title = request.json.get('title')
  if 'description' in request.json:
    g.ruleset.description = request.json.get('description')

  g.ruleset.save()
  response = {
    "message": "updated",
    "item": {
      "title": g.ruleset.title,
      "description": g.ruleset.description
    }
  }
  return jsonify(response)