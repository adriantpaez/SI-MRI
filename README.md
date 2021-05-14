# Information Recovery System

> This project is the final evaluation of the Information Systems subject of the Computer Science degree at the University of Havana.

The implementation is based on SVD as matrix decomposition to perform searches. All the theoretical explanation is in the report.

The application is divided into 3 main parts or stages:

- Process the initial set of documents and construction of a vocabulary.
- Calculation of all the necessary metrics such as **TF**, **DF**, and the weight matrix **W** which is decomposed using the SVD method.
- Perform searches and retrieve relevant documents (for this a web interface was made).

## Structure

```
├── CISI/
│   └── ...
├── CRAN
│   └── ...
├── Makefile
├── mri/
│   ├── config.py
│   ├── database.py
│   ├── data.sqlite
│   ├── fixdatabase.py
│   ├── __init__.py
│   ├── main.py
│   ├── metrics.py
│   ├── parse.py
│   ├── svd.py
│   ├── utils.py
│   └── W.npy
├── README.md
├── requirements.txt
└── server.py
```

- `CISI` and` CRAN` contain all the documents of the two databases used.
- The `mri` folder contains the entire python implementation of the recovery system (it is the center of this project).
  - `congig.py` contains a configuration variable` AlreadyInit` that indicates if all previous calculations are already in the database. The value of this variable must be controlled by the user.
  - `database.py` contains all the code that guarantees the persistence (in a SQLite database) of the computations performed on the collection. All documents, vocabulary and metrics **TF** and **DF** are stored in the database.
  - `data.sqlite` is the SQLite database used to ensure data persistence and not have to recalculate all the metrics every time. _Initially it should not be in the project, it is generated during the processing of the information._
  - `main.py` in this file the fundamental classes like` Vocabulary`, `DataSet` and` MRI` are implemented.
  - `metrics.py` contains the` metrics` function to check the accuracy of the system against the current set of documents.
  - `parse.py` has the necessary functions to process the files with the data (documents, queries and relations).
  - `svd.py` contains the` factorization` function that is used to factor the **W** matrix.
  - `utils.py` contains various helper functions.
  - `W.npy` This file persistently saves the **W** matrix for later use without having to recalculate. _Initially it should not be in the project, it is generated during the processing of the information._ 
- The `server.py` file is run to start the entire recovery process and to be able to use the web interface.

## Install requirements

First, you need install requirements listed at file requirements.txt

```bash
pip install -r requirements.txt
```

## Running for first time

If you are running for the first time, make sure the `AlreadyInit` var is set to `False`. This is needed to compute for the first time all metrics. Then in the root project directory, run this command:
```bash
python server.py
```
You can see then the progress of computations and at the end, a server is up on http://localhost:5000. To open the web interface please go to this address: http://localhost:5000/index.html.

## Running again

If you already run for the first time, then you can set to `True` the `AlreadyInit` var, and run the command again. In this case, the server starts immediately.
