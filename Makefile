install:
	python -m pip install -r requirements.txt
	python -m pip install -e src/

build:
	sudo docker-compose build

start:
	sudo docker-compose up -d

stop:
	sudo docker-compose down
