from tests.fixtures.client import client
from tests.fixtures.first_ruleset import first_ruleset
from rulesets.models.ruleset import Ruleset
import pytest
from bson.objectid import ObjectId

@pytest.fixture
def update_title(client):
  def inner_method():
    return client.put('/rulesets/' + str(pytest.ruleset._id), json={'title': 'other title'})
  return inner_method

@pytest.fixture
def update_empty_title(client):
  def inner_method():
    return client.put('/rulesets/' + str(pytest.ruleset._id), json={'title': ''})
  return inner_method

@pytest.fixture
def update_unknown_id(client):
  def inner_method():
    return client.put('/rulesets/' + str(ObjectId()), json={'title': 'other title'})
  return inner_method

@pytest.fixture
def update_description(client):
  def inner_method():
    return client.put('/rulesets/' + str(pytest.ruleset._id), json={'description': 'updated desc'})
  return inner_method

def setup_function(function):
  Ruleset.objects.raw({}).delete()
  pytest.ruleset = Ruleset(title='test title', description='test description').save()

def test_title_update_status_code_in_nominal_case(update_title):
  assert update_title().status_code == 200

def test_title_update_response_body_in_nominal_case(update_title):
  assert update_title().get_json()['message'] == 'updated'

def test_title_update_in_database(first_ruleset, update_title):
  update_title()
  assert first_ruleset().title == 'other title'

def test_update_empty_title_status_code(update_empty_title):
  assert update_empty_title().status_code == 400

def test_update_empty_title_response_body(update_empty_title):
  assert update_empty_title().get_json()['message'] == 'title_empty'

def test_update_empty_title_in_database(first_ruleset, update_empty_title):
  update_empty_title()
  assert first_ruleset().title == 'test title'

def test_description_update_status_code(update_description):
  assert update_description().status_code == 200

def test_description_update_responde_body(update_description):
  assert update_description().get_json()['message'] == 'updated'

def test_description_update_in_database(first_ruleset, update_description):
  update_description()
  assert first_ruleset().description == 'updated desc'

def test_update_with_unknown_id_status_code(update_unknown_id):
  assert update_unknown_id().status_code == 404

def test_update_with_unknown_id_response_body(update_unknown_id):
  assert update_unknown_id().get_json()['message'] == 'not_found'