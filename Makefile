CURRENT_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
PYTHONPATH := $(CURRENT_DIR):$(PYTHONPATH)
DJANGO_SETTINGS_MODULE := settings
ARDUINO_BOARD := uno
DAEMON_LOG_FILE := /tmp/bmo_controller_daemon.log

export PYTHONPATH DJANGO_SETTINGS_MODULE

default: mkvirtualenv install syncdb

run: run-web run-daemon

install:
	@pip install -r $(CURRENT_DIR)/requirements.txt

mkvirtualenv:
	@bash -ic 'source virtualenvwrapper.sh && mkvirtualenv -q bmo_controller' &>/dev/null

run-web:
	@django-admin.py runserver

run-gunicorn:
	gunicorn wsgi -c gunicorn.conf

run-daemon:
	nohup django-admin.py bmo_daemon >$(DAEMON_LOG_FILE) 2>&1 &

syncdb:
	@django-admin.py syncdb

arduino-upload:
	cd arduino && ino clean && ino build -m $(ARDUINO_BOARD) && ino upload -m $(ARDUINO_BOARD)
