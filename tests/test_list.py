import pytest
from bson.objectid import ObjectId
from rulesets.models import Account, Ruleset, Session
from tests.fixtures import client

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

@pytest.fixture
def list_request(client):
  return lambda p: client.get('/rulesets', query_string = p)

@pytest.fixture
def list(list_request):
  return list_request({'session_id': pytest.session.token})

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
  assert list.status_code == 200

def test_empty_list_response_body(list):
  assert list.get_json() == []

def test_populated_list_status_code(list):
  Ruleset(title='test title', description='test description').save()
  assert list.status_code == 200

def test_populated_list_response_body(list):
  assert list.get_json() == [
    {
      '_id': str(Ruleset.objects[0]._id),
      'title': 'test title',
      'description': 'test description'
    }
  ]