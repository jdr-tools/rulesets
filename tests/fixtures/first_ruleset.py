import pytest
from rulesets.models.ruleset import Ruleset

@pytest.fixture
def first_ruleset():
  def inner_method():
    return Ruleset.objects.raw({'_id': pytest.ruleset._id})[0]
  return inner_method