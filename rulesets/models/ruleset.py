from pymodm import MongoModel, fields
from rulesets.models.account import Account
import pdb

class Ruleset(MongoModel):
  """
    A ruleset is a set of rules defining how to play an RPG.
    .. todo:: Add the whole systme of entities to be able to populate the ruleset.
  """

  title = fields.CharField(min_length=6)
  description = fields.CharField()
  created_at = fields.DateTimeField()
  updated_at = fields.DateTimeField()
  creator_id = fields.ObjectIdField()

  def creator():
    if creator_id is None:
      return None
    return Account.objects.raw({'_id' : creator_id})

  def to_h(self):
    return {
      'title': self.title,
      'description': self.description
    }

  class Meta:
    collection_name = 'arkaan_rulesets'
    final = True