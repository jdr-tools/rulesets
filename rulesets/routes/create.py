from bson.objectid import ObjectId
from flask import jsonify, request
from rulesets.models.ruleset import Ruleset
import pdb, sys
from rulesets.routes.blueprints import rulesets_blueprint

@rulesets_blueprint.route("", methods=['POST'])
def create():
  ruleset = Ruleset(
    _id=ObjectId(),
    title=request.json['title'],
    description=request.json.get('description', '')
  )
  ruleset.save()

  return jsonify({"message": "created", "item": ruleset.to_h()}), 201