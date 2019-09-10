import pytest
from bson.objectid import ObjectId
from rulesets.models import Account, Ruleset, Session
from tests.fixtures import client

def setup_module():
  pytest.ruleset = Ruleset.objects.create(
    title='test title',
    description='test description'
  )

@pytest.fixture
def get_item(client):
  return lambda p={}: client.get('/rulesets/' + str(pytest.ruleset._id), query_string=p)

@pytest.fixture
def get_unknown_item(client):
  return lambda: client.get('/rulesets/' + str(ObjectId()), query_string={'session_id': pytest.session.token})

def setup_function():
  pytest.ruleset = Ruleset(title='test title', description='test description').save()

def test_missing_session_id_status_code(client):
  assert client.get('/rulesets').status_code == 400

def test_missing_session_id_response_body(client):
  response_body = client.get('/rulesets').get_json()
  assert response_body == {
    'status': 400,
    'field': 'session_id',
    'error': 'required'
  }

def test_empty_session_id_status_code(get_item):
  assert get_item({'session_id': None}).status_code == 400

def test_empty_session_id_response_body(get_item):
  response_body = get_item({'session_id': None}).get_json()
  assert response_body == {
    'status': 400,
    'field': 'session_id',
    'error': 'required'
  }

def test_unknown_session_id_status_code(get_item):
  response = get_item({'session_id': str(ObjectId())})
  assert response.status_code == 404

def test_unknown_session_id_response_body(get_item):
  response = get_item({'session_id': str(ObjectId())})
  assert response.get_json() == {
    'status': 404,
    'field': 'session_id',
    'error': 'unknown'
  }

def test_get_existing_item_status_code(get_item):
  assert get_item({'session_id': pytest.session.token}).status_code == 200

def test_get_existing_item_response_body(get_item):
  assert get_item({'session_id': pytest.session.token}).get_json() == {
    'title': 'test title',
    'description': 'test description'
  }

def test_get_unknown_item_status_code(get_unknown_item):
  assert get_unknown_item().status_code == 404

def test_get_unknown_item_response_body(get_unknown_item):
  assert get_unknown_item().get_json() == {
    'status': 404,
    'field': 'ruleset_id',
    'error': 'unknown'
  }
