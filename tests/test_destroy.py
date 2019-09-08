from rulesets.models.ruleset import Ruleset
from tests.fixtures.client import client
import pytest
from bson.objectid import ObjectId

def setup_function(function):
  Ruleset.objects.raw({}).delete()
  pytest.ruleset = Ruleset(title='test title', description='test description').save()

def test_delete_status_code_in_nominal_case(client):
  response = client.delete('/rulesets/' + str(pytest.ruleset._id))
  assert response.status_code == 200

def test_delete_request_body_in_nominal_case(client):
  response = client.delete('/rulesets/' + str(pytest.ruleset._id))
  assert response.get_json()['message'] == 'deleted'

def test_ruleset_deletion_in_nominal_case(client):
  client.delete('/rulesets/' + str(pytest.ruleset._id))
  assert Ruleset.objects.raw({}).count() == 0

def test_ruleset_deletion_status_code_when_id_not_found(client):
  response = client.delete('/rulesets/' + str(ObjectId()))
  assert response.status_code == 404

def test_ruleset_deletion_body_when_id_not_found(client):
  response = client.delete('/rulesets/' + str(ObjectId()))
  assert response.get_json()['message'] == 'not_found'