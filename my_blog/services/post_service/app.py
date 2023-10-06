# post_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

posts = [
     {'id': 1, 'user_id': 1, 'post': 'Hello, world!'},
    {'id': 2, 'user_id': 2, 'post': 'My first blog post'}
]

@app.route('/')
def hello_world():
    return 'Hello, Post Service!'

@app.route('/post/<int:id>')
def post(id):
    post_by_id = [post for post in posts if post["id"] == id]
    post_info = None
    if len(post_by_id) > 0:
        post_info = post_by_id[0]

    # Get user info from User Service
    if post_info:
        response = requests.get(f'https://myuserserviceboyuan.azurewebsites.net/user/{post_info["user_id"]}')
        if response.status_code == 200:
            post_info['user'] = response.json()

    return jsonify(post_info)


# Endpoint to add a new post
@app.route('/posts', methods=['POST'])
def add_post():
    # Parse the 'done' status from request, default to False if it's not provided
    user_id = request.json.get('user_id', '')
    post = request.json.get('post', '')

    # Create a new post object
    new_post = {
        'id': len(posts) + 1,  # Set ID as the next number in sequence
        'user_id': user_id, 
        'post': post  
    }

    # Add the new post to the posts list
    posts.append(new_post)

    # Return the added post with a status code indicating resource creation
    return jsonify({'post': new_post}), 201

# Endpoint to update an existing post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    # Initialize the post variable as None
    post_update = None
    # Loop through the posts list
    for post in posts:
        if post["id"] == post_id:  # If the post with the given ID is found
            post_update = post
            break
    # If post is not found after looping
    if post_update is None:
        return jsonify({'error': 'Post not found'}), 404
    # Update post attributes with data from the request, use existing value if not provided
    post_update['user_id'] = request.json.get('user_id', post_update['user_id'])
    post_update['post'] = request.json.get('post', post_update['post'])
    # Return the updated post
    return jsonify({'post': post_update})

# Endpoint to delete a post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts  # Reference the global posts list
    # Initialize the post variable as None
    post_del = None
    # Loop through the posts list
    for post in posts:
        if post["id"] == post_id:  # If the post with the given ID is found
            post_del = post
            break
    # If post is not found after looping
    if post_del is None:
        return jsonify({'error': 'Post not found'}), 404
    # Remove the found post from the posts list
    posts.remove(post_del)
    # Return a success message
    return jsonify({'result': 'Post deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5001)