from tests.fixtures.client import client

def test_creation_status_without_title(client):
  response = client.post('/rulesets', json={'description': 'test description'})
  assert response.status_code == 400

def test_creation_body_without_title(client):
  response = client.post('/rulesets', json={'description': 'test description'})
  assert response.get_json() == {'message': 'title_not_given'}

def test_creation_status_with_short_title(client):
  response = client.post('/rulesets', json={'title': 'short', 'description': 'test'})
  assert response.status_code == 400

def test_creation_body_with_short_title(client):
  response = client.post('/rulesets', json={'title': 'short', 'description': 'test'})
  assert response.get_json() == {'message': 'title_too_short'}

def test_creation_status_in_nominal_case(client):
  response = client.post('/rulesets', json={'title': 'long enough', 'description': 'test'})
  assert response.status_code == 201

def test_creation_message_in_nominal_case(client):
  response = client.post('/rulesets', json={'title': 'long enough', 'description': 'test'})
  assert response.get_json()['message'] == 'created'

def test_creation_title_in_nominal_case(client):
  response = client.post('/rulesets', json={'title': 'long enough', 'description': 'test'})
  assert response.get_json()['item']['title'] == 'long enough'

def test_creation_description_in_nominal_case(client):
  response = client.post('/rulesets', json={'title': 'long enough', 'description': 'test'})
  assert response.get_json()['item']['description'] == 'test'