from rulesets.models.ruleset import Ruleset
from flask import jsonify, request
from rulesets import app
from bson.objectid import ObjectId

@app.route("/rulesets/<ruleset_id>", methods=['PUT'])
def update(ruleset_id):
  try:
    ruleset = Ruleset.objects.raw({"_id": ObjectId(ruleset_id)})[0]

    if 'title' in request.json:
      if request.json.get('title') == '':
        return jsonify({'message': 'title_empty'}), 400
      ruleset.title = request.json.get('title')
    if 'description' in request.json:
      ruleset.description = request.json.get('description')

    ruleset.save()
    response = {
      "message": "updated",
      "item": {
        "title": ruleset.title,
        "description": ruleset.description
      }
    }
  except Ruleset.DoesNotExist:
    return jsonify(message="not_found", id=ruleset_id), 404
  return jsonify(response)