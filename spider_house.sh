#!/usr/bin/env bash
echo 'begin to spider house data...'
cd /usr/project/hzdata
nohup python house.py > log/house.log 2>&1 &
nohup python bl_house.py > log/bl_house.log 2>&1 &
