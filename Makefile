SRC = ncfd

venv:
	python3 -m venv venv
deps:
	. venv/bin/activate && pip install -r requirements.txt

deps-dev:
	. venv/bin/activate && pip install -r requirements.dev.txt

lint:
	. venv/bin/activate && flake8 ${SRC}

fmt:
	. venv/bin/activate && black ${SRC}
