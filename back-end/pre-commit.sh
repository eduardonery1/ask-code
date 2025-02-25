#!/bin/bash

autopep8 --in-place -a *.py && isort *.py && flake8 *.py
