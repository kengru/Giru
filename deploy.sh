#!/usr/bin/env bash

#the project dir must be the cwd
git pull
pipenv install -e .

reboot