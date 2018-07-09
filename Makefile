docs:
	@mkdir -p docs
	@python -m adoc html . > docs/index.html

.PHONY: docs
