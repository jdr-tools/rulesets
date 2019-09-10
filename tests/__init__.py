import os, pytest, sys
from rulesets.models import Account, Ruleset, Session

os.environ['MONGODB_URL'] = 'mongodb://localhost:27017/arkaan_tests'

myPath = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
sys.path.insert(0, myPath)

from rulesets import rulesets

def setup_module():
  Account.objects.raw({}).delete()
  Session.objects.raw({}).delete()
  Ruleset.objects.raw({}).delete()

  pytest.account = Account.objects.create(email='courtois.vincent@outlook.com')
  pytest.session = Session.objects.create(
    creator_id = pytest.account._id,
    token = 'super secret token'
  )

def teardown_module(function):
  Ruleset.objects.raw({}).delete()
  Session.objects.raw({}).delete()
  Ruleset.objects.raw({}).delete()