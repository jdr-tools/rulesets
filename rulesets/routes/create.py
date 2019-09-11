from bson.objectid import ObjectId
from flask import jsonify, request
from ..models import Ruleset
from .blueprints import rulesets_blueprint

@rulesets_blueprint.route('', methods=['POST'])
def create():
  ruleset = Ruleset.objects.create(
    _id=ObjectId(),
    title=request.json['title'],
    description=request.json.get('description', '')
  )

  return jsonify(message = 'created', item = ruleset.to_h()), 201