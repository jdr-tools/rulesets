from bson.objectid import ObjectId
from flask import jsonify, request, g
from ..models import Ruleset, Session
from .blueprints import rulesets_blueprint

@rulesets_blueprint.route('/<ruleset_id>', methods = ['PUT'])
def update(ruleset_id) -> tuple:
  if 'title' in request.json:
    g.ruleset.title = request.json.get('title')

  if 'description' in request.json:
    g.ruleset.description = request.json.get('description')

  g.ruleset.save()
  return jsonify(
    message = 'updated',
    item = {
      'title': g.ruleset.title,
      'description': g.ruleset.description
    }
  )