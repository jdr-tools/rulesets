import os, pytest, sys

os.environ['MONGODB_URL'] = 'mongodb://localhost:27017/arkaan_tests'

myPath = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
sys.path.insert(0, myPath)

sys.stdout.write(myPath)

from flaskr import flaskr

@pytest.fixture
def client():
  client = flaskr.app.test_client()
  flaskr.app.config['TESTING'] = True
  yield client

def test_creation_status_without_title(client):
  response = client.post('/rulesets', json={'description': 'test description'})
  assert response.status_code == 400

def test_creation_body_without_title(client):
  response = client.post('/rulesets', json={'description': 'test description'})
  assert response.get_json() == {'message': 'title_not_given'}