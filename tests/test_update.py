from tests.fixtures.client import client
from tests.fixtures.first_ruleset import first_ruleset
from rulesets.models.ruleset import Ruleset
from rulesets.models.account import Account
from rulesets.models.session import Session
import pytest
from bson.objectid import ObjectId

def setup_module():
  Ruleset.objects.delete()
  Session.objects.delete()

  pytest.account = Account.objects.create(email='courtois.vincent@outlook.com')
  pytest.session = Session.objects.create(
    creator_id = pytest.account._id,
    token = 'super secret token'
  )

def teardown_module(function):
  Ruleset.objects.delete()
  Session.objects.delete()
  Ruleset.objects.delete()

@pytest.fixture
def empty_update(client):
  return lambda json: client.put('/rulesets/test', json=json)

@pytest.fixture
def update_title(client):
  return lambda t='other title': client.put('/rulesets/' + str(pytest.ruleset._id), json={
    'title': t,
    'session_id': pytest.session.token
  })

@pytest.fixture
def update_empty_title(client):
  return lambda: client.put('/rulesets/' + str(pytest.ruleset._id), json={
    'title': '',
    'session_id': pytest.session.token
  })

@pytest.fixture
def update_unknown_id(client):
  return lambda: client.put('/rulesets/' + str(ObjectId()), json={
    'title': 'other title',
    'session_id': pytest.session.token
  })

@pytest.fixture
def update_description(client):
  return lambda: client.put('/rulesets/' + str(pytest.ruleset._id), json={
    'description': 'updated desc',
    'session_id': pytest.session.token
  })

def setup_function(function):
  Ruleset.objects.delete()
  pytest.ruleset = Ruleset(title='test title', description='test description').save()

def test_missing_session_id_status_code(empty_update):
  assert empty_update({}).status_code == 400

def test_missing_session_id_response_body(empty_update):
  assert empty_update({}).get_json() == {
    'status': 400,
    'field': 'session_id',
    'error': 'required'
  }

def test_empty_session_id_status_code(empty_update):
  response = empty_update({'session_id': None})
  assert response.status_code == 400

def test_empty_session_id_response_body(empty_update):
  response = empty_update({'session_id': None})
  assert response.get_json() == {
    'status': 400,
    'field': 'session_id',
    'error': 'required'
  }

def test_unknown_session_id_status_code(empty_update):
  response = empty_update({'session_id': str(ObjectId())})
  assert response.status_code == 404

def test_unknown_session_id_response_body(empty_update):
  response = empty_update({'session_id': str(ObjectId())})
  assert response.get_json() == {
    'status': 404,
    'field': 'session_id',
    'error': 'unknown'
  }

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
  assert update_empty_title().get_json() == {
    'status': 400,
    'field': 'title',
    'error': 'too_short'
  }

def test_too_short_title_update_status_code(update_title):
  assert update_title('test').status_code == 400

def test_too_short_title_update_response_body(update_title):
  assert update_title('test').get_json() == {
    'status': 400,
    'field': 'title',
    'error': 'too_short'
  }

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
  assert update_unknown_id().get_json() == {
    'status': 404,
    'field': 'ruleset_id',
    'error': 'unknown'
  }
