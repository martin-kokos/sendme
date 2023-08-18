#!/bin/bash
poetry run uvicorn sendme.app:app --host 0.0.0.0 --port 9999
