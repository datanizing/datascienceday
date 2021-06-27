#!/bin/bash
exec uvicorn wsgi:app --host=0.0.0.0 --port=8080
#gunicorn wsgi:application --bind=0.0.0.0:8080 --access-logfile=- --config /etc/config/config.py