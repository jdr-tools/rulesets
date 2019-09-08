from rulesets import rulesets
import pytest

@pytest.fixture
def client():
  client = rulesets.app.test_client()
  rulesets.app.config['TESTING'] = True
  yield client