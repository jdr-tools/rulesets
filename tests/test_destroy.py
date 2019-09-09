from rulesets.models.account import Account
from rulesets.models.ruleset import Ruleset
from rulesets.models.session import Session
from tests.fixtures.client import client
import pytest
from bson.objectid import ObjectId

def setup_module():
  Account.objects.delete()
  Session.objects.delete()

  pytest.account = Account.objects.create(email='courtois.vincent@outlook.com')
  pytest.session = Session.objects.create(
    creator_id = pytest.account._id,
    token = 'super secret token'
  )

def teardown_module(function):
  Ruleset.objects.raw({}).delete()
  Session.objects.raw({}).delete()

def setup_function(function):
  Ruleset.objects.delete()
  pytest.ruleset = Ruleset(title='test title', description='test description').save()

def teardown_function(function):
  Ruleset.objects.delete()

def test_missing_session_id_status_code(client):
  assert client.delete('/rulesets/test').status_code == 400

def test_missing_session_id_response_body(client):
  response_body = client.delete('/rulesets/test').get_json()
  assert response_body == {'message': 'session_id_required'}

def test_empty_session_id_status_code(client):
  response = client.delete('/rulesets/test', query_string={'session_id': None})
  assert response.status_code == 400

def test_empty_session_id_response_body(client):
  response = client.delete('/rulesets/test', query_string={'session_id': None})
  assert response.get_json() == {'message': 'session_id_required'}

def test_unknown_session_id_status_code(client):
  response = client.delete('/rulesets/test', query_string={'session_id': str(ObjectId())})
  assert response.status_code == 404

def test_unknown_session_id_response_body(client):
  response = client.delete('/rulesets/test', query_string={'session_id': str(ObjectId())})
  assert response.get_json() == {'message': 'session_id_unknown'}

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
  assert response.get_json()['message'] == 'not_found'

def test_element_not_deleted_when_not_found(client):
  client.delete('/rulesets/' + str(ObjectId()), query_string={'session_id': pytest.session.token})
  assert Ruleset.objects.count() == 1