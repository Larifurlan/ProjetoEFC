test:
	pytest -v

cov:
	pytest --cov=.

lint:
	ruff check .

type:
	mypy --strict src/

complexity:
	radon cc . -s -a
