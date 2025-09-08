from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'GET':
        # Get query parameters
        sort_field = request.args.get('sort')
        direction = request.args.get('direction', 'asc')

        # Make a copy so sorting doesn't affect the original POSTS order
        results = POSTS.copy()

        if sort_field:
            # Validate sort field
            if sort_field not in ["title", "content"]:
                return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400

            # Validate direction
            if direction not in ["asc", "desc"]:
                return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

            # Perform sorting
            reverse = True if direction == "desc" else False
            results.sort(key=lambda post: post[sort_field].lower(), reverse=reverse)

        return jsonify(results)

    if request.method == 'POST':
        data = request.get_json()
        new_post = {
            "id": str(uuid.uuid4()),
            "title": data.get("title"),
            "content": data.get("content"),
        }
        POSTS.append(new_post)
        return jsonify(new_post), 201

@app.route('/api/posts/<id>', methods=['DELETE', 'PUT'])
def modify_post(id):
    if request.method == 'DELETE':
        for post in POSTS:
            if str(post["id"]) == str(id):
                POSTS.remove(post)
                return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
        return jsonify({"message": f"Post with id {id} does not exist."}), 404

    if request.method == 'PUT':
        data = request.get_json()
        for post in POSTS:
            if str(post["id"]) == str(id):
                post["title"] = data.get("title", post["title"])
                post["content"] = data.get("content", post["content"])
                return jsonify(post), 200
        return jsonify({"message": f"Post with id {id} does not exist."}), 404

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title', '').lower()
    content = request.args.get('content', '').lower()
    results = []
    for post in POSTS:
        if title:
            title_match = title in post["title"].lower()
        else:
            title_match = True

        if content:
            content_match = content in post["content"].lower()
        else:
            content_match = True

        if title_match and content_match:
            results.append(post)

    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)