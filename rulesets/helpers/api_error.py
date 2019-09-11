from flask import jsonify

def api_error(status, error_string):
  """
    Formats an API as it is excpected from the rest of the API.
    :param status: the HTTP status, you want to respond with.
    :type status: integer
    :params error_string: a string of the form <field>.<error>
    :type error_string: string
    :return The JSON formatted error, and the HTTP code, to be used by Flask.
    :rtype set
  """
  field, error = error_string.split('.')
  err_json = jsonify({
    'status': status,
    'field': field,
    'error': error
  })
  return err_json, status