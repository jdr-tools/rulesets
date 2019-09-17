import pytest
from bson.objectid import ObjectId
from rulesets.models import Account, Ruleset, Session
from tests.fixtures import client

class CreateRequestable():
  """This class is just a superclass to create rulesets more easily."""
  @pytest.fixture
  def create(self, client):
    return lambda p: client.post('/rulesets', json = {**p, 'session_id': pytest.session.token})

@pytest.mark.describe('Create - nominal case')
class TestCreateNominalCase(CreateRequestable):

  @classmethod
  def teardown_class(self):
    Ruleset.objects.delete()

  @pytest.mark.it('Returns a 200 (OK) Status code')
  def test_creation_status_in_nominal_case(self, create):
    response = create({'title': 'long enough', 'description': 'test'})
    assert response.status_code == 201

  @pytest.mark.it('Returns the correct message')
  def test_creation_message_in_nominal_case(self, create):
    response = create({'title': 'long enough', 'description': 'test'})
    assert response.get_json()['message'] == 'created'

  @pytest.mark.it('Returns the correct title')
  def test_creation_title_in_nominal_case(self, create):
    response = create({'title': 'long enough', 'description': 'test'})
    assert response.get_json()['item']['title'] == 'long enough'

  @pytest.mark.it('Returns the correct description')
  def test_creation_description_in_nominal_case(self, create):
    response = create({'title': 'long enough', 'description': 'test'})
    assert response.get_json()['item']['description'] == 'test'

@pytest.mark.describe('Create without title')
class TestWithoutTitle(CreateRequestable):

  @pytest.mark.it('Returns a 400 (Bad Request) Status code')
  def test_creation_status_without_title(self, create):
    response = create({'description': 'test description'})
    assert response.status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_creation_body_without_title(self, create):
    response = create({'description': 'test description'})
    assert response.get_json() == {
      'status': 400,
      'field': 'title',
      'error': 'required'
    }

@pytest.mark.describe('Create with title too short')
class TestCreateWithShortTitle(CreateRequestable):

  @pytest.mark.it('Returns a 200 (OK) Status code')
  def test_creation_status_with_short_title(self, create):
    response = create({'title': 'short', 'description': 'test'})
    assert response.status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_creation_body_with_short_title(self, create):
    response = create({'title': 'short', 'description': 'test'})
    assert response.get_json() == {
      'status': 400,
      'field': 'title',
      'error': 'too_short'
    }

@pytest.mark.describe('Create without giving session ID')
class TestCreateWithoutSessionId():

  @pytest.mark.it('Returns a 400 (Bad Request) Status code')
  def test_missing_session_id_status_code(self, client):
    assert client.post('/rulesets').status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_missing_session_id_response_body(self, client):
    response_body = client.post('/rulesets').get_json()
    assert response_body == {
      'status': 400,
      'field': 'session_id',
      'error': 'required'
    }

@pytest.mark.describe('Create with empty session ID')
class TestCreateWithEmptySessionId():

  @pytest.mark.it('Returns a 400 (Bad Request) Status code')
  def test_empty_session_id_status_code(self, client):
    response = client.post('/rulesets', json={'session_id': None})
    assert response.status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_empty_session_id_response_body(self, client):
    response = client.post('/rulesets', json={'session_id': None})
    assert response.get_json() == {
      'status': 400,
      'field': 'session_id',
      'error': 'required'
    }

@pytest.mark.describe('Create with unknown session ID')
class TestCreateWithUnknownSessionId():

  @pytest.mark.it('Returns a 404 (Not Found) Status code')
  def test_unknown_session_id_status_code(self, client):
    response = client.post('/rulesets', json={'session_id': str(ObjectId())})
    assert response.status_code == 404

  @pytest.mark.it('Returns the correct body')
  def test_unknown_session_id_response_body(self, client):
    response = client.post('/rulesets', json={'session_id': str(ObjectId())})
    assert response.get_json() == {
      'status': 404,
      'field': 'session_id',
      'error': 'unknown'
    }


