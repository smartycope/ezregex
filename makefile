.PHONY: docs stubs

docs:
	sphinx-build -b html docs docs/_build/html

stubs:
	stubgen -p ezregex -o stubs/
	cp stubs/ezregex/**/*.pyi ezregex/