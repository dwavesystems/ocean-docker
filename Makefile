.PHONY: latest tags is-clean release
SHELL = /bin/bash

latest: env
	@env/bin/python generate.py dockerfiles
	@env/bin/python generate.py readme

tags: env
	@env/bin/python generate.py tags

env:
	python -m venv env && env/bin/pip install -r requirements.txt

is-clean:
	@[[ -n $$(git status --porcelain) ]] && echo 'Git working tree dirty. Aborting.' && exit 1

release: is-clean latest
release: ocean_version = $(shell env/bin/python generate.py version)
	git add -u
	git commit -m 'Generate Ocean $(ocean_version) dockerfiles, tags and readme'
