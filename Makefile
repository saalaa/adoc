default: docs

docs:
	python -m adoc -o docs/index.html .

clean:
	rm -rf .pytest_cache .eggs .coverage adoc.egg-info build dist __pycache__ adoc/__pycache__

.PHONY: help docs clean
