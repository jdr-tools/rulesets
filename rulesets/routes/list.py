from rulesets import app
from flask import jsonify
from rulesets.models.ruleset import Ruleset

@app.route("/rulesets", methods=['GET'])
def list():
  rulesets = []
  for ruleset in Ruleset.objects.raw({}):
    rulesets.append({
      "_id": str(ruleset._id),
      "title": ruleset.title,
      "description": ruleset.description
    })
  return jsonify(rulesets)