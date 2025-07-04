#!/bin/bash
gunicorn gui_app:app --bind 0.0.0.0:$PORT
