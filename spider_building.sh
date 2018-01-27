#!/usr/bin/env bash
echo 'begin to spider building data...'
nohup python /usr/project/hzdata/building.py > /usr/project/hzdata/log/building.log 2>&1 &