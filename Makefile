run:
	SETTINGS_FILE=./config/development.cfg ./env/bin/python ./main.py

update:
	./env/bin/pip install -r ./requirements.txt

init:
	virtualenv ./env
