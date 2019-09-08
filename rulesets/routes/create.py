from bson.objectid import ObjectId
from flask import jsonify, request
from rulesets import app
from rulesets.models.ruleset import Ruleset
import pdb, sys

@app.route("/rulesets", methods=['POST'])
def create():
  if 'title' not in app.parsed_body:
    return jsonify({"message": "title_not_given"}), 400
  elif len(app.parsed_body['title']) < 6:
    return jsonify({"message": "title_too_short"}), 400

  ruleset = Ruleset(
    _id=ObjectId(),
    title=app.parsed_body['title'],
    description=app.parsed_body.get('description', '')
  )
  ruleset.save()

  return jsonify({"message": "created", "item": ruleset.to_h()}), 201