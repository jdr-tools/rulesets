from pymodm import MongoModel, fields

class Session(MongoModel):
  token = fields.CharField()
  creator_id = fields.ObjectIdField()

  class Meta:
    collection_name = 'arkaan_authentication_sessions'
    final = True
    ignore_unknown_fields = True