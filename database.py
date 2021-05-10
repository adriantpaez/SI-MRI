import json
from tqdm import tqdm
import sqlite3
import nltk
from nltk.tokenize import word_tokenize
import re

con = sqlite3.connect('data.sqlite')


def load_docs(docs_file):
    print(f'Loading documents from {docs_file}')
    c = con.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id integer PRIMARY KEY,
            title text NOT NULL,
            author text NOT NULL,
            text text NOT NULL
        );
    """)
    con.commit()
    with open(docs_file) as file:
        data = json.load(file)
        sql = 'INSERT INTO documents (title, author, text) VALUES (?, ?, ?)'
        for key in tqdm(data):
            c.execute(sql, (data[key]['title'], data[key]['author'], data[key]['text']))
        con.commit()


def init_vocabulary_table():
    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS  vocabulary")
    con.commit()
    c.execute("""
                CREATE TABLE vocabulary (
                    id integer PRIMARY KEY,
                    value text NOT NULL UNIQUE
                );
            """)
    con.commit()


def load_vocabulary(vocabulary_file):
    print(f'Loading vocabulary from {vocabulary_file}')
    c = con.cursor()
    init_vocabulary_table()
    with open(vocabulary_file) as f:
        for line in tqdm(f):
            c.execute(f'INSERT INTO vocabulary (value) VALUES (\'{line[:-1]}\')')
        con.commit()


def load_vocabulary2():
    print(f'Build vocabulary from documents')
    c = con.cursor()
    init_vocabulary_table()
    # Check if documents exists
    cursosr = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents';")
    if cursosr.rowcount == 0:
        raise Exception("documents table do not exits")
    documents = con.execute("SELECT title, author, text FROM documents")
    s = set(["NN", "NNS", "NNP", "NNPS", "VB", "VBG", "VBD", "VBN", "VBP", "VBZ", "JJ", "JJR", "JJS"])
    for document in tqdm(documents, total=documents_len(), unit=' document'):
        for i in range(3):
            for word in nltk.pos_tag(word_tokenize(document[i])):
                w = word[0].lower()
                if word[1] in s and re.match(r'([a-z]|[0-9]).*', w) and len(w) > 1:
                    try:
                        c.execute("INSERT INTO vocabulary (value) VALUES (?)", (w,))
                    except sqlite3.IntegrityError:
                        continue
        con.commit()


def vocabulary_vector():
    vocabulary = con.execute("SELECT value FROM Vocabulary")
    result = sorted([x[0] for x in vocabulary])
    return result


def calculate_tf():
    print("Computing TF for each word in vocabulary")
    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS  tf")
    con.commit()
    c.execute("""
            CREATE TABLE tf (
                vocabularyId integer NOT NULL,
                documentId integer NOT NULL,
                tf integer NOT NULL,
                PRIMARY KEY (vocabularyId, documentId)
            );
        """)
    con.commit()
    vocabulary = con.execute("SELECT id, value FROM vocabulary")
    for word in tqdm(vocabulary, total=vocabulary_len(), unit=' word'):
        documents = con.execute("SELECT id, title, author, text FROM documents")
        for document in documents:
            tf = len(re.findall(re.escape(word[1]), document[1], re.IGNORECASE))
            tf += len(re.findall(re.escape(word[1]), document[2], re.IGNORECASE))
            tf += len(re.findall(re.escape(word[1]), document[3], re.IGNORECASE))
            # tf = document[1].lower().count(word[1]) + document[2].count(word[1]) + document[3].count(word[1])
            con.execute(
                f'INSERT INTO tf (vocabularyId, documentId, tf) VALUES (\'{word[0]}\', \'{document[0]}\', \'{tf}\')')
        con.commit()


def calculate_df():
    print("Computing DF for each word in vocabulary")
    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS  df")
    con.commit()
    c.execute("""
                CREATE TABLE df (
                    vocabularyId integer PRIMARY KEY,
                    df integer NOT NULL
                );
            """)
    con.commit()
    vocabulary = con.execute("SELECT id, value FROM vocabulary")
    for word in tqdm(vocabulary, total=vocabulary_len(), unit=' word'):
        df = list(con.execute(f"SELECT COUNT(*) FROM tf WHERE vocabularyId == {word[0]} AND tf > 0"))
        c.execute(f"INSERT INTO df (vocabularyId, df) VALUES ('{word[0]}', '{df[0][0]}')")
        con.commit()


def vocabulary_len():
    c = con.cursor()
    vl = list(c.execute("SELECT COUNT(*) FROM vocabulary"))
    return vl[0][0]


def documents_len():
    c = con.cursor()
    dl = list(c.execute("SELECT COUNT(*) FROM documents"))
    return dl[0][0]


def TF(i, j):
    c = con.cursor()
    tf = list(c.execute(f"SELECT tf FROM tf WHERE vocabularyId == {i + 1} AND documentId == {j + 1}"))
    return tf[0][0]


def DF(i):
    c = con.cursor()
    df = list(c.execute(f"SELECT df FROM df WHERE vocabularyId == {i + 1}"))
    return df[0][0]
