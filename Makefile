ifeq ("$(wildcard ./config/live.cfg)", "")
	SETTINGS=./config/development.cfg
else
	SETTINGS=./config/live.cfg
endif

ifeq ("$(VIRTUAL_ENV)", "")
  ENV=. env/bin/activate;
endif

run:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./main.py

init:
	virtualenv ./env

update:
	$(ENV) pip install -r ./requirements.txt --use-mirrors

clean:
	rm -rf ./env


db:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py createdb

data: tickets tokens shifts

tickets:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py createtickets

tokens:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py addtokens

shifts:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py createroles
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py createshifts


checkreconcile:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py reconcile -f var/data.ofx
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py reconcile -f var/data-eur.ofx

reallyreconcile:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py reconcile -f var/data.ofx -d
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py reconcile -f var/data-eur.ofx -d


warnexpire:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py warnexpire

expire:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py expire


shell:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py shell

testemails:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py testemails

admin:
	$(ENV) SETTINGS_FILE=$(SETTINGS) python ./utils.py makeadmin

test:
	$(ENV) SETTINGS_FILE=./config/test.cfg flake8 ./models ./views --ignore=E501,F403,E302,F401,E128,W293,W391,E251,E303,E502,E111,E225,E221,W291,E124,W191,E101,E201,E202,E261,E127,E265,E231

