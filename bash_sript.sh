#!/usr/bin/env bash
/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip
pip install Flask
pip install sqlalchemy
pip install gunicorn