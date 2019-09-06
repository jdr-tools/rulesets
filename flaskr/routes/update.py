from flaskr.models.ruleset import Ruleset
from flask import jsonify, request
from flaskr import app

@app.route("/rulesets/<ruleset_id>", methods=['PUT'])
def update(ruleset_id):
  try:
    ruleset = Ruleset.objects.raw({"_id": ObjectId(ruleset_id)})[0]
    ruleset.title = request.json['title']
    ruleset.description = request.json['description']
    ruleset.save()
    response = {
      "message": "created",
      "item": {
        "title": ruleset.title,
        "description": ruleset.description
      }
    }
  except Ruleset.DoesNotExist:
    return jsonify(message="not_found", id=ruleset_id), 404
  return jsonify(response)