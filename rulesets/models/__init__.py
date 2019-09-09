import pymodm, os

from rulesets.models.account import Account
from rulesets.models.ruleset import Ruleset
from rulesets.models.session import Session

pymodm.connection.connect(os.getenv('MONGODB_URL'))