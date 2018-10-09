pwd := $(shell pwd)

all: compile run

compile:
	@echo compile
	go build .

run:
	./git-trends fetch

docker_build:
	@echo building docker image
	docker build -t ipv/python:3.6 .

docker_run:
	@echo run docker container
	docker run --name ipv --rm -v $(pwd)/data:/src/data -it -d ipv/python:3.6 bash
	docker exec -it ipv bash

push:
	@echo push

clean:
	@echo clean
	rm -rf data/raw/*.csv
	rm -rf data/interim/*.csv
	rm -rf data/processed/*.csv
	rm -rf data/processed/*.geojson

test:
	@echo running some tests

venv:
	@echo activate virtualenv
	./source venv/bin/activate

install_requirements:
	pip install -r requirements.txt

freeze_requirements:
	pip freeze > requirements.txt
