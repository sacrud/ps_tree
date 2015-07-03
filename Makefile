all: test

test:
	nosetests --with-coverage --cover-package ps_tree --cover-erase --with-doctest --nocapture
