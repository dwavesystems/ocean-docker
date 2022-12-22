.PHONY: latest tags

latest: env
	@env/bin/python generate.py dockerfiles
	@env/bin/python generate.py readme

tags: env
	@env/bin/python generate.py tags

env:
	python -m venv env && env/bin/pip install -r requirements.txt
