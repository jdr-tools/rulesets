import os, sys, pdb, json
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from rulesets.models.account import Account
from rulesets.models.ruleset import Ruleset
from bson.objectid import ObjectId
from rulesets.routes.blueprints.rulesets import rulesets_blueprint
import rulesets.routes

load_dotenv()
app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(rulesets_blueprint, url_prefix='/rulesets')