from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Dummy data storage
resources = [
    {"id": 1, "name": "Resource 1", "description": "Description of Resource 1"},
    {"id": 2, "name": "Resource 2", "description": "Description of Resource 2"}
]

# Dummy token for authentication
VALID_TOKEN = "your_secret_token"

def token_required(f):
    """Decorator to check for a valid token in the request headers."""
    def decorator(*args, **kwargs):
        # Check if the Authorization header is present and valid
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {VALID_TOKEN}":
            abort(401, description="Unauthorized")
        return f(*args, **kwargs)
    return decorator

@app.route('/api/resources', methods=['GET'])
@token_required
def get_resources():
    """Handles GET requests to retrieve all resources."""
    return jsonify(resources)

@app.route('/api/resources/<int:resource_id>', methods=['GET'])
@token_required
def get_resource(resource_id):
    """Handles GET requests to retrieve a specific resource by ID."""
    resource = next((r for r in resources if r['id'] == resource_id), None)
    if resource is None:
        abort(404, description="Resource not found")
    return jsonify(resource)

@app.route('/api/resources', methods=['POST'])
@token_required
def create_resource():
    """Handles POST requests to create a new resource."""
    if not request.json or 'name' not in request.json:
        abort(400, description="Bad Request: 'name' is required")
    
    resource = {
        'id': len(resources) + 1,
        'name': request.json['name'],
        'description': request.json.get('description', '')
    }
    resources.append(resource)
    return jsonify(resource), 201

@app.route('/api/resources/<int:resource_id>', methods=['PUT'])
@token_required
def update_resource(resource_id):
    """Handles PUT requests to update an existing resource."""
    resource = next((r for r in resources if r['id'] == resource_id), None)
    if resource is None:
        abort(404, description="Resource not found")
    
    if not request.json:
        abort(400, description="Bad Request: Body cannot be empty")
    
    resource['name'] = request.json.get('name', resource['name'])
    resource['description'] = request.json.get('description', resource['description'])
    return jsonify(resource)

@app.route('/api/resources/<int:resource_id>', methods=['DELETE'])
@token_required
def delete_resource(resource_id):
    """Handles DELETE requests to remove a resource."""
    global resources
    resources = [r for r in resources if r['id'] != resource_id]
    return jsonify({'result': 'Resource deleted'}), 200

@app.errorhandler(401)
def unauthorized_error(error):
    """Handles 401 Unauthorized errors."""
    return jsonify({'error': 'Unauthorized access'}), 401

@app.errorhandler(404)
def not_found_error(error):
    """Handles 404 Not Found errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request_error(error):
    """Handles 400 Bad Request errors."""
    return jsonify({'error': 'Bad Request'}), 400

@app.errorhandler(500)
def internal_error(error):
    """Handles 500 Internal Server Error errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
