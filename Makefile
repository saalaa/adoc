docs:
	@mkdir -p docs
	@python -m adoc . > docs/index.html

.PHONY: docs
