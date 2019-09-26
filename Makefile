init:
	pipenv install

test:
	pipenv run pytest --cov=rulesets --testdox tests/