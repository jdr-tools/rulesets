from rulesets import app
from flask import jsonify
from rulesets.models.ruleset import Ruleset
from bson.objectid import ObjectId

@app.route("/rulesets/<ruleset_id>", methods=['GET'])
def item(ruleset_id):
  try:
    ruleset = Ruleset.objects.raw({"_id": ObjectId(ruleset_id)})[0]
  except Ruleset.DoesNotExist:
    return jsonify(message="not_found", id=ruleset_id), 404
  return jsonify(title=ruleset.title, description=ruleset.description)