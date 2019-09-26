import pytest
from bson.objectid import ObjectId
from rulesets.models import Account, Ruleset, Session
from tests.fixtures import client

class TestUpdate():
  def setup_method(self, method):
    Ruleset.objects.delete()
    self.ruleset = Ruleset.objects.create(
      title = 'test title',
      description = 'test description'
    )
    self.id = str(self.ruleset._id)
  def teardown_method(self, method):
    Ruleset.objects.delete()

@pytest.mark.describe('Update without session ID')
class TestWithoutSessionId(TestUpdate):

  @pytest.fixture
  def update(self, client):
    return lambda: client.put(f'/rulesets/{self.id}', json = {})

  @pytest.mark.it('Returns a 400 (Bad Request) Status code')
  def test_status_code(self, update):
    assert update().status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, update):
    assert update().get_json() == {
      'status': 400,
      'field': 'session_id',
      'error': 'required'
    }

@pytest.mark.describe('Update with empty session ID')
class TestWithEmptySessionId(TestUpdate):

  @pytest.fixture
  def update(self, client):
    return lambda: client.put(f'/rulesets/{self.id}', json = {'session_id': None})

  @pytest.mark.it('Returns a 400 (Bad Request) Status code')
  def test_status_code(self, update):
    assert update().status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, update):
    assert update().get_json() == {
      'status': 400,
      'field': 'session_id',
      'error': 'required'
    }

@pytest.mark.describe('Update with unknown session ID')
class TestWithUnknownSessionId(TestUpdate):

  @pytest.fixture
  def update(self, client):
    return lambda: client.put(f'/rulesets/{self.id}', json = {'session_id': 'test_unknwon'})

  @pytest.mark.it('Returns a 404 (Not Found) Status code')
  def test_status_code(self, update):
    assert update().status_code == 404

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, update):
    assert update().get_json() == {
      'status': 404,
      'field': 'session_id',
      'error': 'unknown'
    }

@pytest.mark.describe('')
class TestWithUnknownId(TestUpdate):

  @pytest.fixture
  def update(self, client):
    return lambda: client.put('/rulesets/unknown', json = {
      'title': 'other title',
      'session_id': pytest.session.token
    })

  @pytest.mark.it('Returns a 404 (Not Found) Status code')
  def test_status_code(self, update):
    assert update().status_code == 404

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, update):
    assert update().get_json() == {
      'status': 404,
      'field': 'ruleset_id',
      'error': 'unknown'
    }

@pytest.mark.describe('Nominal case, update of the title')
class TestUpdateTitle(TestUpdate):

  @pytest.fixture
  def update(self, client):
    return lambda: client.put(f'/rulesets/{self.id}', json = {
      'title': 'other title',
      'session_id': pytest.session.token
    })

  @pytest.mark.it('Returns a 200 (OK) Status code')
  def test_status_code(self, update):
    assert update().status_code == 200

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, update):
    assert update().get_json()['message'] == 'updated'

  @pytest.mark.it('Updates the ruleset in the database')
  def test_database_update(self, update):
    update()
    ruleset = Ruleset.objects.raw({'_id': self.ruleset._id})[0]
    assert ruleset.title == 'other title'


@pytest.mark.describe('Update with an empty title')
class TestUpdateEmptyTitle(TestUpdate):

  @pytest.fixture
  def update(self, client):
    return lambda: client.put(f'/rulesets/{self.id}', json = {
      'title': '',
      'session_id': pytest.session.token
    })

  @pytest.mark.it('Returns a 400 (Bad Request) Status code')
  def test_status_code(self, update):
    assert update().status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, update):
    assert update().get_json() == {
      'status': 400,
      'field': 'title',
      'error': 'too_short'
    }

  @pytest.mark.it('Has not updated the title in the database')
  def test_database_update(self, update):
    update()
    ruleset = Ruleset.objects.raw({'_id': self.ruleset._id})[0]
    assert ruleset.title == 'test title'

@pytest.mark.describe('Update with a too short title')
class TestUpdateShortTitle(TestUpdate):

  @pytest.fixture
  def update(self, client):
    return lambda: client.put(f'/rulesets/{self.id}', json = {
      'title': 'test',
      'session_id': pytest.session.token
    })

  @pytest.mark.it('Returns a 400 (Bad Request) Status code')
  def test_status_code(self, update):
    assert update().status_code == 400

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, update):
    assert update().get_json() == {
      'status': 400,
      'field': 'title',
      'error': 'too_short'
    }

  @pytest.mark.it('Has not updated the title in the database')
  def test_database_update(self, update):
    update()
    ruleset = Ruleset.objects.raw({'_id': self.ruleset._id})[0]
    assert ruleset.title == 'test title'

@pytest.mark.describe('Update of the description')
class TestUpdateDescription(TestUpdate):

  @pytest.fixture
  def update(self, client):
    return lambda: client.put(f'/rulesets/{self.id}', json = {
      'description': 'updated desc',
      'session_id': pytest.session.token
    })

  @pytest.mark.it('Returns a 200 (OK) Status code')
  def test_status_code(self, update):
    assert update().status_code == 200

  @pytest.mark.it('Returns the correct body')
  def test_response_body(self, update):
    assert update().get_json()['message'] == 'updated'

  @pytest.mark.it('Updates the ruleset in the database')
  def test_database_update(self, update):
    update()
    ruleset = Ruleset.objects.raw({'_id': self.ruleset._id})[0]
    assert ruleset.description == 'updated desc'