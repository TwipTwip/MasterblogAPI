from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    post_ids = []
    new_id = 0
    for post in POSTS:
        post_ids.append(post['id'])
    new_id = max(post_ids) + 1
    new_post = request.get_json()
    if 'title' not in new_post or 'content' not in new_post:
        return jsonify("Error: Post missing title or content"), 404
    new_post['id'] = new_id
    POSTS.append(new_post)
    return jsonify(POSTS)


def find_post_by_id(post_id):
    for post in POSTS:
        if post['id'] == int(post_id):
            return post


@app.route('/api/posts/<id>', methods=['DELETE'])
def delete_post(id):
    post = find_post_by_id(id)

    if post is None:
        return jsonify("Error: Post not found"), 404

    counter = -1
    for info in POSTS:
        counter += 1
        if info['id'] == int(post['id']):
            del (POSTS[counter])

    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
