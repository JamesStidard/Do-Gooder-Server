init:
	pip install -r requirements.txt
	pip install -e .
db_init:
	python -m dogooder.initialize
test:
	py.test tests
run:
	python -m dogooder.server
