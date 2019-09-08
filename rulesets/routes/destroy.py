from bson.objectid import ObjectId
from rulesets import app
from rulesets.models.ruleset import Ruleset
from flask import jsonify

@app.route("/rulesets/<ruleset_id>", methods=["DELETE"])
def delete(ruleset_id):
  try:
    ruleset = Ruleset.objects.raw({"_id": ObjectId(ruleset_id)})[0]
    ruleset.delete()
  except Ruleset.DoesNotExist:
    return jsonify(message="not_found", id=ruleset_id), 404
  return jsonify(message="deleted")