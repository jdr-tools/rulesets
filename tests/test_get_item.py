from bson.objectid import ObjectId
import pytest
from tests.fixtures.client import client
from rulesets.models.ruleset import Ruleset
from bson.objectid import ObjectId

@pytest.fixture
def get_item(client):
  def inner_method():
    return client.get('/rulesets/' + str(pytest.ruleset._id))
  return inner_method

@pytest.fixture
def get_unknown_item(client):
  def inner_method():
    return client.get('/rulesets/' + str(ObjectId()))
  return inner_method

def setup_function():
  pytest.ruleset = Ruleset(title='test title', description='test description').save()

def teardown_function():
  Ruleset.objects.raw({}).delete()

def test_get_existing_item_status_code(get_item):
  assert get_item().status_code == 200

def test_get_existing_item_response_body(get_item):
  assert get_item().get_json() == {
    'title': 'test title',
    'description': 'test description'
  }

def test_get_unknown_item_status_code(get_unknown_item):
  assert get_unknown_item().status_code == 404

def test_get_unknown_item_response_body(get_unknown_item):
  assert get_unknown_item().get_json()['message'] == 'not_found'