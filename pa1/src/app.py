import json
from flask import Flask, request

app = Flask(__name__)

post_counter = 2
comment_counter = 0
posts = {
    0: {
      "id": 0,
      "upvotes": 1,
      "title": "My cat is the cutest!",
      "link": "https://i.imgur.com/jseZqNK.jpg",
      "username": "alicia98",
    },
    1: {
      "id": 1,
      "upvotes": 3,
      "title": "Cat loaf",
      "link": "https://i.imgur.com/TJ46wX4.jpg",
      "username": "alicia98",
    }
}
comments = {}

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/api/posts/')
def get_posts():
    res = {'success': True, 'data': list(posts.values())}
    return json.dumps(res), 200

@app.route('/api/posts/', methods=['POST'])
def create_post():
    global post_counter
    print(request)
    print(request.data)
    post_body = json.loads(request.data)
    title = post_body['title']
    link = post_body['link']
    username = post_body['username']
    post = {
        'id': post_counter,
        'upvotes': 1,
        'title': title,
        'link': link,
        'username': username
    }
    posts[post_counter] = post
    post_counter += 1
    return json.dumps({'success': True, 'data': post}), 201

@app.route('/api/post/<int:id>/')
def get_post(id):
    if id in posts:
        post = posts[id]
        return json.dumps({'success': True, 'data': post}), 200
    return json.dumps({'success': False, 'error': 'Post id not in range'}), 404

@app.route('/api/post/<int:id>/', methods=['DELETE'])
def delete_post(id):
    if id in posts:
        post = posts[id]
        del posts[id]
        return json.dumps({'success': True, 'data': post}), 200
    return json.dumps({'success': False, 'error': 'Post id not in range'}), 404

@app.route('/api/post/<int:id>/comments/')
def get_comments(id):
    if id in comments and id in posts:
        res = {'success': True, 'data': list(comments[id].values())}
        return json.dumps(res), 200
    return json.dumps({'success': False, 'error': 'Post id of comment not found'}), 404

@app.route('/api/post/<int:id>/comment/', methods=['POST'])
def post_comment(id):
    if id in posts:
        global comment_counter
        comment_body = json.loads(request.data)
        text = comment_body['text']
        username = comment_body['username']
        comment = {
            'id': comment_counter,
            'upvotes': 1,
            'text': text,
            'username': username
        }
        if id in comments:
            comments[id][comment_counter] = comment
        else:
            comments[id] = {comment_counter:comment}
        comment_counter += 1
        return json.dumps({'success': True, 'data': comment}), 201
    return json.dumps({'success': False, 'error': 'Post does not exist to comment on'}), 404

@app.route('/api/post/<int:pid>/comment/<int:cid>/', methods=['POST'])
def edit_comment(pid, cid):
    comment_body = json.loads(request.data)
    text = comment_body['text']
    comments[pid][cid]['text'] = text
    return json.dumps({'success': True, 'data': comments[pid][cid]}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

