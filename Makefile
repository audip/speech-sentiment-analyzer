.PHONY: init test

init:
	pip install -r requirements.txt

test:
	nosetests test

