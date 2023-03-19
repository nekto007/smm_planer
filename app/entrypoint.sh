#!/bin/bash

if [ $# == 0 ]; then
  python3 main.py
else
  exec "$@"
fi
