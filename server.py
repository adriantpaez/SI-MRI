import string

from flask import Flask, request, jsonify

from mri import database as db
from mri.main import mri

app = Flask(__name__, static_url_path='', static_folder='static')


@app.route('/search')
def search():
    query = request.args.get('query')
    query = query.translate(str.maketrans('', '', string.punctuation))
    query = query.split(' ')
    ids = [int(x) for x in mri(query, k=10)]
    return jsonify(ids)


@app.route('/documentPreview')
def get_document_preview():
    id = int(request.args.get('id'))
    docP = db.get_document_preview(id)
    return jsonify(docP)


@app.route('/document')
def get_document():
    id = int(request.args.get('id'))
    doc = db.get_document(id)
    return jsonify(doc)


if __name__ == "__main__":
    app.run()
