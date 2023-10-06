# user_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
]
    
@app.route('/')
def hello_world():
    return 'Hello, User Service!'

@app.route('/user/<int:id>')
def user(id):
    users_by_id = [user for user in users if user["id"] == id]
    user_info = None
    if len(users_by_id) > 0:
        user_info = users_by_id[0]
    return jsonify(user_info)

# Endpoint to add a new user
@app.route('/users', methods=['POST'])
def add_user():
    # Parse the 'done' status from request, default to False if it's not provided
    name = request.json.get('name', '')
    email = request.json.get('email', '')

    # Create a new user object
    new_user = {
        'id': len(users) + 1,  # Set ID as the next number in sequence
        'name': name, 
        'email': email  
    }

    # Add the new user to the users list
    users.append(new_user)

    # Return the added user with a status code indicating resource creation
    return jsonify({'user': new_user}), 201

# Endpoint to update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Initialize the user variable as None
    user_update = None
    # Loop through the users list
    for user in users:
        if user["id"] == int(user_id):  # If the user with the given ID is found
            user_update = user
            break
    # If user is not found after looping
    if user_update is None:
        return jsonify({'error': 'User not found'}), 404
    # Update user attributes with data from the request, use existing value if not provided
    user_update['name'] = request.json.get('name', user_update['name'])
    user_update['email'] = request.json.get('email', user_update['email'])
    # Return the updated user
    return jsonify({'user': user_update})

# Endpoint to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users  # Reference the global users list
    # Initialize the user variable as None
    user_del = None
    # Loop through the users list
    for user in users:
        if user["id"] == user_id:  # If the user with the given ID is found
            user_del = user
            break
    # If user is not found after looping
    if user_del is None:
        return jsonify({'error': 'User not found'}), 404
    # Remove the found user from the users list
    users.remove(user_del)
    # Return a success message
    return jsonify({'result': 'User deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5000)