# post_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
comments = [
    {'id': 1, 'user_id': '1', 'post_id': '2', 'comment': 'Amazing comment!'},
    {'id': 2, 'user_id': '2', 'post_id': '2', 'comment': 'I did not know that'}
]

@app.route('/')
def hello_world():
    return 'Hello, Comment Service!'

@app.route('/comment/<int:id>')
def get_comment(id):
    comment_by_id = [comment for comment in comments if comment["id"] == id]
    comment_info = None
    if len(comment_by_id) > 0:
        comment_info = comment_by_id[0]
    
    
    if comment_info:
        # Get user info from User Service
        if comment_info["user_id"]:
            try: 
                response = requests.get(f'https://myuserservice.azurewebsites.net/user/{comment_info["user_id"]}')
                if response.status_code == 200:
                    comment_info['user'] = response.json()
            except:
                pass
                
        # Get post info from Post Service
        if comment_info["post_id"]:
            try:
                response = requests.get(f'https://mypostservice.azurewebsites.net/post/{comment_info["post_id"]}')                
                if response.status_code == 200:
                    print("got post")
                    comment_info['post'] = response.json()                
            except:
                pass

    return jsonify(comment_info)

# Endpoint to add a new comment
@app.route('/comments', methods=['POST'])
def add_comment():
    # Parse the 'done' status from request, default to False if it's not provided
    user_id = request.json.get('user_id', '')
    post_id = request.json.get('post_id', '')
    comment = request.json.get('comment', '')
    # Create a new comment object
    new_comment = {
        'id': len(comments) + 1,  # Set ID as the next number in sequence
        'user_id': user_id, 
        'post_id': post_id,
        'comment': comment
    }

    # Add the new comment to the comments list
    comments.append(new_comment)

    # Return the added comment with a status code indicating resource creation
    return jsonify({'comment': new_comment}), 201

# Endpoint to update an existing comment
@app.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    # Initialize the comment variable as None
    comment_update = None
    # Loop through the comments list
    for comment in comments:
        if comment["id"] == comment_id:  # If the comment with the given ID is found
            comment_update = comment
            break
    # If comment is not found after looping
    if comment_update is None:
        return jsonify({'error': 'Comment not found'}), 404
    # Update comment attributes with data from the request, use existing value if not provided
    comment_update['user_id'] = request.json.get('user_id', comment_update['user_id'])
    comment_update['post_id'] = request.json.get('post_id', comment_update['post_id'])
    comment_update['comment'] = request.json.get('comment', comment_update['comment'])
    # Return the updated comment
    return jsonify({'comment': comment_update})

# Endpoint to delete a comment
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    global comments  # Reference the global comments list
    # Initialize the comment variable as None
    comment_del = None
    # Loop through the comments list
    for comment in comments:
        if comment["id"] == comment_id:  # If the comment with the given ID is found
            comment_del = comment
            break
    # If comment is not found after looping
    if comment_del is None:
        return jsonify({'error': 'Comment not found'}), 404
    # Remove the found comment from the comments list
    comments.remove(comment_del)
    # Return a success message
    return jsonify({'result': 'Comment deleted successfully'}), 200


if __name__ == '__main__':
    app.run(port=5002)