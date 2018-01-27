#!/usr/bin/env bash
echo 'begin to spider house data...'
nohup python /usr/project/hzdata/house.py > /usr/project/hzdata/log/house.log 2>&1 &