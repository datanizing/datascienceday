#!/bin/bash
exec uvicorn app.app:app --host=0.0.0.0 --port=8080

