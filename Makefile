ADOC_OPTS=-d docs/faq.md -d docs/examples.md

help: # This help message
	@echo Valid make targets:
	@awk '/^[a-z]/ { print $1; }' < Makefile \
		| sed 's/^/\n  /' \
		| sed 's/: #/\n   /'

docs: docs/index.html docs/django-project.html docs/appengine-project.html \
		docs/flask-project.html

docs/index.html: # Build project documentation
	python -m adoc -v $(ADOC_OPTS) --html $@ .

docs/django-project.html: # Build Django sample documentation
	python -m adoc -v --html $@ examples/django-project

docs/appengine-project.html: # Build Google AppEngine sample documentation
	python -m adoc -v -s hello_world_api.py -s greetings_api.py \
		--html $@ examples/appengine-project

docs/flask-project.html: # Build Flask sample documentation
	python -m adoc -v -s app.py --strip-docstrings --html $@ examples/flask-project

serve: # Start a live server on project documentation
	python -m adoc -v $(ADOC_OPTS) --http .

release: clean build upload

clean: # Cleanup temporary files
	rm -rf .pytest_cache .eggs .coverage adoc.egg-info build dist __pycache__ \
		adoc/__pycache__

build: # Build Python release artifact
	python setup.py bdist_wheel

upload: # Upload release artifact to PyPi
	twine upload dist/*

.PHONY: help docs release clean build upload

# Documentation is phony as well.
.PHONY: docs/index.html
.PHONY: docs/django-project.html
.PHONY: docs/appengine-project.html
.PHONY: docs/flask-project.html
