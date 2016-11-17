#!/usr/bin/env bash
if [[ $EUID -ne 0 ]]; then
    sudo pip install -r requirements.txt
else
    pip install -r requirements.txt
fi