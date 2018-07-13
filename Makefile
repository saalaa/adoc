ADOC_OPTS=-d docs/faq.md

default:
	python -m adoc $(ADOC_OPTS) -o docs/index.html .

serve:
	python -m adoc $(ADOC_OPTS) --serve .

clean:
	rm -rf .pytest_cache .eggs .coverage adoc.egg-info build dist __pycache__ adoc/__pycache__

build:
	python setup.py bdist_wheel

upload:
	twine upload dist/*

release: build upload

.PHONY: help docs clean build upload release
