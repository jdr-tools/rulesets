from pymodm import MongoModel, fields

class Account(MongoModel):
  email = fields.CharField()

  class Meta:
    collection_name = 'arkaan_accounts'
    final = True
    ignore_unknown_fields = True