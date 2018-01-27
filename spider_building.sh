#!/usr/bin/env bash
echo 'begin to spider building data...'
cd /usr/project/hzdata
nohup python building.py > log/building.log 2>&1 &