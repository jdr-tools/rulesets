import pytest
from bson.objectid import ObjectId
from rulesets.models import Account, Ruleset, Session
from tests.fixtures import client

def setup_function(function):
  Ruleset.objects.delete()
  pytest.ruleset = Ruleset(title='test title', description='test description').save()

def teardown_function(function):
  Ruleset.objects.delete()

def test_missing_session_id_status_code(client):
  assert client.delete('/rulesets/test').status_code == 400

def test_missing_session_id_response_body(client):
  response_body = client.delete('/rulesets/test').get_json()
  assert response_body == {
    'status': 400,
    'field': 'session_id',
    'error': 'required'
  }

def test_empty_session_id_status_code(client):
  response = client.delete('/rulesets/test', query_string={'session_id': None})
  assert response.status_code == 400

def test_empty_session_id_response_body(client):
  response = client.delete('/rulesets/test', query_string={'session_id': None})
  assert response.get_json() == {
    'status': 400,
    'field': 'session_id',
    'error': 'required'
  }

def test_unknown_session_id_status_code(client):
  response = client.delete('/rulesets/test', query_string={'session_id': str(ObjectId())})
  assert response.status_code == 404

def test_unknown_session_id_response_body(client):
  response = client.delete('/rulesets/test', query_string={'session_id': str(ObjectId())})
  assert response.get_json() == {
    'status': 404,
    'field': 'session_id',
    'error': 'unknown'
  }

def test_delete_status_code_in_nominal_case(client):
  response = client.delete('/rulesets/' + str(pytest.ruleset._id), query_string={'session_id': pytest.session.token})
  assert response.status_code == 200

def test_delete_request_body_in_nominal_case(client):
  response = client.delete('/rulesets/' + str(pytest.ruleset._id), query_string={'session_id': pytest.session.token})
  assert response.get_json()['message'] == 'deleted'

def test_ruleset_deletion_in_nominal_case(client):
  client.delete('/rulesets/' + str(pytest.ruleset._id), query_string={'session_id': pytest.session.token})
  assert Ruleset.objects.raw({}).count() == 0

def test_ruleset_deletion_status_code_when_id_not_found(client):
  response = client.delete('/rulesets/' + str(ObjectId()), query_string={'session_id': pytest.session.token})
  assert response.status_code == 404

def test_ruleset_deletion_body_when_id_not_found(client):
  response = client.delete('/rulesets/' + str(ObjectId()), query_string={'session_id': pytest.session.token})
  assert response.get_json() == {
    'status': 404,
    'field': 'ruleset_id',
    'error': 'unknown'
  }

def test_element_not_deleted_when_not_found(client):
  client.delete('/rulesets/' + str(ObjectId()), query_string={'session_id': pytest.session.token})
  assert Ruleset.objects.count() == 1