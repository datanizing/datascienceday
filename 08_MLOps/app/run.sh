#!/bin/bash
exec gunicorn wsgi:application --bind=0.0.0.0:8080 --access-logfile=- --config /etc/config/config.py