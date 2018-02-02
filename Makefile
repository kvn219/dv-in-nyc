venv:
	venv/bin/activate

save_requirements:
	pip freeze > requirements.txt

run: clean
	python ipv/main.py

clean:
	rm -rf data/raw/*.csv
	rm -rf data/interim/*
	rm -rf data/processed/*