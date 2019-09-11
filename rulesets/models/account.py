from pymodm import MongoModel, fields

class Account(MongoModel):
  """
    class representing a user account, to be completed later.
    .. note:: Until adding all the needed properties, the created accounts might bug the ruby API.
    .. todo:: Add the complete representation of the account, derived from the Arkaan gem.
  """

  email = fields.CharField()

  class Meta:
    collection_name = 'arkaan_accounts'
    final = True
    ignore_unknown_fields = True