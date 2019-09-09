from tests.fixtures.client import client
from rulesets.models.ruleset import Ruleset
import pytest

def teardown_function(function):
  Ruleset.objects.raw({}).delete()

def test_empty_list_status_code(client):
  assert client.get('/rulesets').status_code == 200

def test_empty_list_response_body(client):
  assert client.get('/rulesets').get_json() == []

def test_populated_list_status_code(client):
  Ruleset(title='test title', description='test description')
  assert client.get('/rulesets').status_code == 200

def test_populated_list_response_body(client):
  ruleset = Ruleset(title='test title', description='test description').save()
  assert client.get('/rulesets').get_json() == [
    {
      '_id': str(ruleset._id),
      'title': 'test title',
      'description': 'test description'
    }
  ]