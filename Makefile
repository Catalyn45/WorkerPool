install:
	python -m pip install -r requirements.txt || python3 -m pip install -r requirements.txt
	python -m pip install -e src/ || python3 -m pip install -e src/
