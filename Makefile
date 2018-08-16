ADOC_OPTS=-d docs/faq.md -d docs/examples.md

default: docs/index.html docs/django-project.html docs/appengine-project.html

docs/index.html:
	python -m adoc -v $(ADOC_OPTS) --html $@ .

docs/django-project.html:
	python -m adoc -v --html $@ examples/django-project

docs/appengine-project.html:
	python -m adoc -v -s main.py --html $@ examples/appengine-project

serve:
	python -m adoc -v $(ADOC_OPTS) --http .

clean:
	rm -rf .pytest_cache .eggs .coverage adoc.egg-info build dist __pycache__ \
		adoc/__pycache__

build:
	python setup.py bdist_wheel

upload:
	twine upload dist/*

release: clean build upload

.PHONY: help docs clean build upload release

# Documentation is phony as well.
.PHONY: docs/index.html
.PHONY: docs/django-project.html
.PHONY: docs/appengine-project.html
