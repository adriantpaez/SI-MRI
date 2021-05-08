import json
from tqdm import tqdm
import sqlite3

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


def load_vocabulary(vocabulary_file):
    print(f'Loading vocabulary from {vocabulary_file}')
    c = con.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id integer PRIMARY KEY,
                value text NOT NULL
            );
        """)
    con.commit()
    with open(vocabulary_file) as f:
        for line in tqdm(f):
            c.execute(f'INSERT INTO vocabulary (value) VALUES (\'{line[:-1]}\')')
        con.commit()


def vocabulary_vector():
    vocabulary = con.execute("SELECT value FROM Vocabulary")
    result = sorted([x[0] for x in vocabulary])
    return result


def calculate_tf():
    print("Computing TF for each words in vocabulary")
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
    for word in vocabulary:
        documents = con.execute("SELECT id, title, author, text FROM documents")
        for document in documents:
            tf = document[1].count(word[1]) + document[2].count(word[1]) + document[3].count(word[1])
            con.execute(
                f'INSERT INTO tf (vocabularyId, documentId, tf) VALUES (\'{word[0]}\', \'{document[0]}\', \'{tf}\')')
    con.commit()


def calculate_df():
    print("Computing DF for each words in vocabulary")
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
    for word in vocabulary:
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
