default: docs

docs:
	@mkdir -p docs
	@python -m adoc . > docs/index.html

clean:
	@rm -rf .pytest_cache .eggs .coverage adoc.egg-info build dist __pycache__ adoc/__pycache__

.PHONY: docs clean
