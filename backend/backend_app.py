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
    """This is the function that shows all the posts but queries can be
    inputted to sort how the posts are shown"""
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    if sort is None or direction is None:
        return jsonify(POSTS)

    if sort == 'title' and direction == 'asc':
        sorted_posts = sorted(POSTS, key=lambda x: x['title'])
        return jsonify(sorted_posts)

    if sort == 'title' and direction == 'desc':
        sorted_posts = sorted(POSTS, key=lambda x: x['title'], reverse=True)
        return jsonify(sorted_posts)
    if sort == 'content' and direction == 'asc':
        sorted_posts = sorted(POSTS, key=lambda x: x['content'])
        return jsonify(sorted_posts)

    if sort == 'content' and direction == 'desc':
        sorted_posts = sorted(POSTS, key=lambda x: x['content'], reverse=True)
        return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """This route adds a post to the list of blog posts"""
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
    """This is a simple function that was created so that code wasn't repeated"""
    for post in POSTS:
        if post['id'] == int(post_id):
            return post


@app.route('/api/posts/<id>', methods=['DELETE'])
def delete_post(id):
    """This route finds the post with the inputted id and deletes it"""
    post = find_post_by_id(id)

    if post is None:
        return jsonify("Error: Post not found"), 404

    counter = -1
    for info in POSTS:
        counter += 1
        if info['id'] == int(post['id']):
            del (POSTS[counter])

    return jsonify(POSTS)


@app.route('/api/posts/<id>', methods=['PUT'])
def update_post(id):
    """This route updates the post with the new inputted info"""
    post = find_post_by_id(id)

    if post is None:
        return jsonify("Error: Post not found"), 404

    new_data = request.get_json()
    post.update(new_data)

    return jsonify(POSTS)


@app.route('/api/posts/search', methods=['GET'])
def search():
    """This route searches through the posts and shows the related info to what was inputted"""
    title = request.args.get('title')
    content = request.args.get('content')
    posts_to_return = []
    if title is None or content is None:
        return posts_to_return
    for post in POSTS:
        if title in post['title'] or content in post['content']:
            posts_to_return.append(post)
    return jsonify(posts_to_return)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
