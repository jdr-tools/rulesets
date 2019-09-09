from tests.fixtures.client import client
import pytest
from rulesets.models.account import Account
from rulesets.models.ruleset import Ruleset
from rulesets.models.session import Session
from bson.objectid import ObjectId

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
def create(client):
  def inner_method(parameters):
    return client.post('/rulesets', json={**parameters, 'session_id': pytest.session.token})
  return inner_method

def test_missing_session_id_status_code(client):
  assert client.post('/rulesets').status_code == 400

def test_missing_session_id_response_body(client):
  response_body = client.post('/rulesets').get_json()
  assert response_body == {'message': 'session_id_required'}

def test_empty_session_id_status_code(client):
  response = client.post('/rulesets', json={'session_id': None})
  assert response.status_code == 400

def test_empty_session_id_response_body(client):
  response = client.post('/rulesets', json={'session_id': None})
  assert response.get_json() == {'message': 'session_id_required'}

def test_unknown_session_id_status_code(client):
  response = client.post('/rulesets', json={'session_id': str(ObjectId())})
  assert response.status_code == 404

def test_unknown_session_id_response_body(client):
  response = client.post('/rulesets', json={'session_id': str(ObjectId())})
  assert response.get_json() == {'message': 'session_id_unknown'}

def test_creation_status_without_title(create):
  response = create({'description': 'test description'})
  assert response.status_code == 400

def test_creation_body_without_title(create):
  response = create({'description': 'test description'})
  assert response.get_json() == {'message': 'title_not_given'}

def test_creation_status_with_short_title(create):
  response = create({'title': 'short', 'description': 'test'})
  assert response.status_code == 400

def test_creation_body_with_short_title(create):
  response = create({'title': 'short', 'description': 'test'})
  assert response.get_json() == {'message': 'title_too_short'}

def test_creation_status_in_nominal_case(create):
  response = create({'title': 'long enough', 'description': 'test'})
  assert response.status_code == 201

def test_creation_message_in_nominal_case(create):
  response = create({'title': 'long enough', 'description': 'test'})
  assert response.get_json()['message'] == 'created'

def test_creation_title_in_nominal_case(create):
  response = create({'title': 'long enough', 'description': 'test'})
  assert response.get_json()['item']['title'] == 'long enough'

def test_creation_description_in_nominal_case(create):
  response = create({'title': 'long enough', 'description': 'test'})
  assert response.get_json()['item']['description'] == 'test'