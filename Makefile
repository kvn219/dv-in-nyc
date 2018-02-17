venv:
	venv/bin/activate

install_requirements:
	pip install -r requirements.txt

freeze_requirements:
	pip freeze > requirements.txt

run: clean
	python ipv/main.py

clean:
	rm -rf data/raw/*.csv
	rm -rf data/interim/*.csv
	rm -rf data/processed/*.csv
	rm -rf data/processed/*.geojson