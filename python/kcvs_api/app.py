#!flask/bin/python
# abort - 404
# make_response - Flask generates the 404 response by 
#   default. Since this is a web service client applications 
#   will expect that we always respond with JSON, so we 
#   need to improve our 404 error handler
from flask import Flask, jsonify, abort, make_response, request
from key_column_value_store import KeyColumnValueStore

app = Flask(__name__)

store = KeyColumnValueStore(path='/tmp/codetestdata')

@app.route('/')
def home():
    return "Hello, World!"

# get keys
@app.route('/api/v1/keys', methods = ['GET'])
def index():
	return jsonify( { 'data': store.get_keys() } )

# get_key
@app.route('/api/v1/keys/<string:key_id>', methods = ['GET'])
def show_key(key_id):
	sorted_list = store.get_key(key_id)
	if sorted_list == []:
		abort(404)
	return jsonify( {'data': sorted_list} )

# set
@app.route('/api/v1/value', methods = ['POST'])
def create():
    if not request.json or not 'key' in request.json or not 'col' in request.json:
        abort(400)
    store.set(request.json['key'], request.json['col'], request.json.get('val', ""))
    return jsonify( { 'success' : store.get(request.json['key'], request.json['col']) }), 201

# get
@app.route('/api/v1/keys/<string:key_id>/cols/<string:col_id>', methods = ['GET'])
def show(key_id, col_id):
	val = store.get(key_id, col_id)
	if val == None:
		abort(404)
	return jsonify( { 'data': { 'key': key_id, 'col': col_id, 'val': val }} )

# delete
@app.route('/api/v1/keys/<string:key_id>/cols/<string:col_id>', methods = ['DELETE'])
def delete(key_id, col_id):
	store.delete(key_id, col_id)
	return jsonify( { 'result': True } )

# delete_key
@app.route('/api/v1/keys/<string:key_id>', methods = ['DELETE'])
def delete_key(key_id):
	store.delete_key(key_id)
	return jsonify( { 'result': True } )

# ERROR HANDLING
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

if __name__ == '__main__':
    app.run(debug = True)