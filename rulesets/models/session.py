from pymodm import MongoModel, fields

class Session(MongoModel):
  """
    A session is the object representing the connection of a user to the API.
  """

  token = fields.CharField()
  creator_id = fields.ObjectIdField()

  class Meta:
    collection_name = 'arkaan_authentication_sessions'
    final = True
    ignore_unknown_fields = True