.PHONY: update dockerfiles readme tags is-clean git-branch git-commit git-push release gh-pr pr
SHELL = /bin/bash

update: dockerfiles readme

dockerfiles: env
	@env/bin/python generate.py dockerfiles

readme: env
	@env/bin/python generate.py readme

tags: env
	@env/bin/python generate.py tags

env:
	python -m venv env && env/bin/pip install -r requirements.txt

is-clean:
	@if [[ -n "$$(git status --porcelain)" ]]; then echo 'Git working tree dirty. Aborting.'; exit 1; fi

git-branch:
	git checkout -b 'build-ocean-$(ocean_version)'

git-commit:
	git add -u
	git commit -m 'Generate Ocean $(ocean_version) dockerfiles, tags and readme'

git-push:
	git push

release: ocean_version = $(shell env/bin/python generate.py version)
release: is-clean git-branch update git-commit

gh-pr: ocean_version = $(shell env/bin/python generate.py version)
gh-pr:
	gh pr create --title 'Build Ocean $(ocean_version) images'

pr: ocean_version = $(shell env/bin/python generate.py version)
pr: git-push gh-pr
