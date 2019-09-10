import pytest
import pdb
from bson.objectid import ObjectId
from rulesets.models import Account, Ruleset, Session
from tests.fixtures import client

def teardown_function():
  Ruleset.objects.delete()

@pytest.fixture
def list_request(client):
  return lambda p: client.get('/rulesets', query_string = p)

@pytest.fixture
def list(list_request):
  return lambda: list_request({'session_id': pytest.session.token})

def test_missing_session_id_status_code(client):
  assert client.get('/rulesets').status_code == 400

def test_missing_session_id_response_body(client):
  response_body = client.get('/rulesets').get_json()
  assert response_body == {
    'status': 400,
    'field': 'session_id',
    'error': 'required'
  }

def test_empty_session_id_status_code(list_request):
  assert list_request({'session_id': None}).status_code == 400

def test_empty_session_id_response_body(list_request):
  response_body = list_request({'session_id': None}).get_json()
  assert response_body == {
    'status': 400,
    'field': 'session_id',
    'error': 'required'
  }

def test_unknown_session_id_status_code(list_request):
  response = list_request({'session_id': str(ObjectId())})
  assert response.status_code == 404

def test_unknown_session_id_response_body(list_request):
  response = list_request({'session_id': str(ObjectId())})
  assert response.get_json() == {
    'status': 404,
    'field': 'session_id',
    'error': 'unknown'
  }

def test_empty_list_status_code(list):
  assert list().status_code == 200

def test_empty_list_response_body(list):
  assert list().get_json() == []

def test_populated_list_status_code(list):
  Ruleset(title='test title', description='test description').save()
  assert list().status_code == 200

def test_populated_list_response_body(list):
  ruleset = Ruleset(title='test title', description='test description').save()
  assert list().get_json() == [
    {
      '_id': str(ruleset._id),
      'title': 'test title',
      'description': 'test description'
    }
  ]