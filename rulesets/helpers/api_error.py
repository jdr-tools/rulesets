from flask import jsonify

def api_error(status, error_string):
  field, error = error_string.split('.')
  err_json = jsonify({
    'status': status,
    'field': field,
    'error': error
  })
  return err_json, status