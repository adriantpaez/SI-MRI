from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/search')
def search():
    query = request.args.get('query')
    print(query)
    return jsonify([1, 2, 3])


@app.route('/document')
def get_document():
    id = int(request.args.get('id'))
    return jsonify({
        'id': id,
        'title': "Some title",
        'author': "Some author",
        'text': "Some text"
    })
