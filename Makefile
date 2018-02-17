pwd := $(shell pwd)


venv:
	venv/bin/activate

install_requirements:
	pip install -r requirements.txt

freeze_requirements:
	pip freeze > requirements.txt

run: clean
	python ipv/main.py

docker_build:
	docker build -t ipv/python:3.6 .

docker_run:
	docker run --name ipv --rm -v $(pwd)/data:/src/data -it -d ipv/python:3.6 bash
	docker exec -it ipv bash

clean:
	rm -rf data/raw/*.csv
	rm -rf data/interim/*.csv
	rm -rf data/processed/*.csv
	rm -rf data/processed/*.geojson