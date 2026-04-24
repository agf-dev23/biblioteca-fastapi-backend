#!/bin/bash
# Arranque para producción

uvicorn main:app --host 0.0.0.0 --port $PORT