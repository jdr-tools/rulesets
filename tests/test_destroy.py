import pytest, pdb
from bson.objectid import ObjectId
from rulesets.models import Account, Ruleset, Session
from tests.fixtures import client

class DestroyRequestable():
  """This class is just a superclass to easily make requests to delete rulesets."""
  @pytest.fixture
  def delete(self, client):
    url = f"/rulesets/{str(self.id)}"
    query_string = {'session_id': pytest.session.token}
    return lambda: client.delete(url, query_string = query_string)

@pytest.mark.describe('Destroy - nominal case')
class TestDestroyNominalCase(DestroyRequestable):

  def setup_method(self):
    self.ruleset = Ruleset.objects.create(title = 'test title', description = 'test description')
    self.id = self.ruleset._id

  def teardown_method(self):
    Ruleset.objects.delete()

  @pytest.mark.it('Returns a 200 (OK) Status code')
  def test_delete_status_code_in_nominal_case(self, delete):
    assert delete().status_code == 200

  @pytest.mark.it('Returns the correct body')
  def test_delete_request_body_in_nominal_case(self, delete):
    assert delete().get_json() == {'message': 'deleted'}

  @pytest.mark.it('Correctly deletes the ruleset from the database')
  def test_ruleset_deletion_in_nominal_case(self, delete):
    response = delete()
    assert Ruleset.objects.raw({'_id': self.ruleset._id}).count() == 0

@pytest.mark.describe('Destroy without giving session ID')
class TestDestroyWithoutSessionId():

  @pytest.mark.it('Returns a 400 (Bad Request) status code')
  def test_status_code(self, client):
    assert client.delete('/rulesets/test').status_code == 400

  @pytest.mark.it('Returns the correct error body')
  def test_response_body(self, client):
    response_body = client.delete('/rulesets/test').get_json()
    assert response_body == {
      'status': 400,
      'field': 'session_id',
      'error': 'required'
    }

@pytest.mark.describe('Destroy with empty session ID')
class TestDestroyWithEmptySessionId():

  @pytest.mark.it('Returns a 400 (Bad Request) status code')
  def test_status_code(self, client):
    response = client.delete('/rulesets/test', query_string={'session_id': None})
    assert response.status_code == 400

  @pytest.mark.it('Returns the correct error body')
  def test_response_body(self, client):
    response = client.delete('/rulesets/test', query_string={'session_id': None})
    assert response.get_json() == {
      'status': 400,
      'field': 'session_id',
      'error': 'required'
    }

@pytest.mark.describe('Destroy with unknown session ID')
class TestDestroyWithUnknownSessionId():

  @pytest.mark.it('Returns a 404 (Not Found) status code')
  def test_unknown_session_id_status_code(self, client):
    response = client.delete('/rulesets/test', query_string={'session_id': str(ObjectId())})
    assert response.status_code == 404

  @pytest.mark.it('Returns the correct error body')
  def test_unknown_session_id_response_body(self, client):
    response = client.delete('/rulesets/test', query_string={'session_id': str(ObjectId())})
    assert response.get_json() == {
      'status': 404,
      'field': 'session_id',
      'error': 'unknown'
    }

@pytest.mark.describe('Destroy with unknown ruleset ID')
class TestDestroyWithUnknowId(DestroyRequestable):

  @classmethod
  def setup_class(self):
    self.id = ObjectId()

  @pytest.mark.it('Returns a 404 (Not Found) status code')
  def test_ruleset_deletion_status_code_when_id_not_found(self, delete):
    assert delete().status_code == 404

  @pytest.mark.it('Returns the correct body')
  def test_ruleset_deletion_body_when_id_not_found(self, delete):
    assert delete().get_json() == {
      'status': 404,
      'field': 'ruleset_id',
      'error': 'unknown'
    }