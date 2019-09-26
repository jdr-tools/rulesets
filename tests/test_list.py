import pytest
from bson.objectid import ObjectId
from rulesets.models import Ruleset
from tests.fixtures import client

class ListRequestable():

  @pytest.fixture
  def list(self, raw_list):
    return lambda: raw_list({'session_id': pytest.session.token})

  @pytest.fixture
  def raw_list(self, client):
    return lambda p: client.get('/rulesets', query_string = p)

@pytest.mark.describe('List - Nominal case without rulesets stored')
class TestEmptyListNominalCase(ListRequestable):

  @pytest.mark.it('Returns a 200 (OK) Status code')
  def test_status_code(self, list):
    assert list().status_code == 200

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, list):
    assert list().get_json() == []

@pytest.mark.describe('List - Nominal case with populated rulesets')
class TestEmptyListNominalCase(ListRequestable):

  def setup_method(self):
    Ruleset.objects.delete()
    self.ruleset = Ruleset.objects.create(title='test title', description='test description')

  def teardown_method(self):
    Ruleset.objects.delete()

  @pytest.mark.it('Returns a 200 (OK) Status code')
  def test_status_code(self, list):
    assert list().status_code == 200

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, list):
    assert list().get_json() == [
      {
        '_id': str(self.ruleset._id),
        'title': 'test title',
        'description': 'test description'
      }
    ]

@pytest.mark.describe('List without session ID')
class TestListWithoutSessionId(ListRequestable):

  @pytest.mark.it('Returns a 400 (Bad Request) Status code')
  def test_status_code(self, raw_list):
    assert raw_list({}).status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, raw_list):
    assert raw_list({}).get_json() == {
      'status': 400,
      'field': 'session_id',
      'error': 'required'
    }

@pytest.mark.describe('List with empty session ID')
class TestListWithEmptySessionId(ListRequestable):

  @pytest.mark.it('Returns a 400 (Bad Request) Status code')
  def test_status_code(self, raw_list):
    assert raw_list({'session_id': None}).status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, raw_list):
    assert raw_list({'session_id': None}).get_json() == {
      'status': 400,
      'field': 'session_id',
      'error': 'required'
    }

@pytest.mark.describe('List with unknown session ID')
class TestListWithUnknownSessionId(ListRequestable):

  @pytest.mark.it('Returns a 404 (Not Found) Status code')
  def test_status_code(self, raw_list):
    response = raw_list({'session_id': str(ObjectId())})
    assert response.status_code == 404

  @pytest.mark.describe('Returns the correct body')
  def test_response_body(self, raw_list):
    assert raw_list({'session_id': str(ObjectId())}).get_json() == {
      'status': 404,
      'field': 'session_id',
      'error': 'unknown'
    }