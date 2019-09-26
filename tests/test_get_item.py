import pytest
from bson.objectid import ObjectId
from rulesets.models import Account, Ruleset, Session
from tests.fixtures import client

class GetRequestable():

  @pytest.fixture
  def get(self, raw_get):
    return lambda: raw_get(self.url, {'session_id': pytest.session.token})

  @pytest.fixture
  def raw_get(self, client):
    return lambda url, parameters: client.get(url, query_string = parameters)

@pytest.mark.describe('Get - Nominal case')
class TestGetNominalCase(GetRequestable):

  @classmethod
  def setup_class(self):
    self.ruleset = Ruleset.objects.create(title = 'test title', description = 'test description')
    self.url = f"/rulesets/{str(self.ruleset._id)}"

  @classmethod
  def teardown_class(self):
    Ruleset.objects.raw({'_id': self.ruleset._id}).delete()

  @pytest.mark.it('Returns a 200 (OK) status code')
  def test_status_code(self, get):
    assert get().status_code == 200

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, get):
    assert get().get_json() == {
      'title': 'test title',
      'description': 'test description'
    }

@pytest.mark.describe('Get item with unknown ID')
class TestWithUnknownId(GetRequestable):

  def setup_class(self):
    self.url = f"/rulesets/{str(ObjectId())}"

  @pytest.mark.it('Returns a 404 (Not Found) Status code')
  def test_status_code(self, raw_get):
    assert raw_get(self.url, {'session_id': pytest.session.token}).status_code == 404

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, raw_get):
    assert raw_get(self.url, {'session_id': pytest.session.token}).get_json() == {
      'status': 404,
      'field': 'ruleset_id',
      'error': 'unknown'
    }

@pytest.mark.describe('Get item without session ID')
class TestGetItemWithoutSessionId():

  @pytest.mark.it('Returns a 400 (Bad Request) Status code')
  def test_status_code(self, client):
    assert client.get('/rulesets').status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, client):
    response_body = client.get('/rulesets').get_json()
    assert response_body == {
      'status': 400,
      'field': 'session_id',
      'error': 'required'
    }

@pytest.mark.describe('Get item with empty session ID')
class TestGetItemWithEmptySessionId(GetRequestable):

  @pytest.mark.it('Returns a 400 (Bad Request) Status code')
  def test_status_code(self, raw_get):
    assert raw_get('/rulesets/any_id', {'session_id': None}).status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, raw_get):
    response_body = raw_get('/rulesets/any_id', {'session_id': None}).get_json()
    assert response_body == {
      'status': 400,
      'field': 'session_id',
      'error': 'required'
    }

@pytest.mark.describe('Get item with unknwon session ID')
class TestGetItemWithUnknownSessionId(GetRequestable):

  @pytest.mark.it('Returns a 404 (Not Found) Status code')
  def test_status_code(self, raw_get):
    response = raw_get('/rulesets/any_id', {'session_id': str(ObjectId())})
    assert response.status_code == 404

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, raw_get):
    response = raw_get('/rulesets/any_id', {'session_id': str(ObjectId())})
    assert response.get_json() == {
      'status': 404,
      'field': 'session_id',
      'error': 'unknown'
    }