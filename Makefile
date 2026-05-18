test:
	pytest -v

cov:
	pytest --cov=.

lint:
	ruff check .

type:
	mypy src/

complexity:
	radon cc . -s -a