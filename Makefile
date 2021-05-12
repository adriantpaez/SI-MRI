
test:
	python mri/test.py

server:
	export FLASK_APP=server.py && flask run
