#!/usr/bin/env bash
echo 'begin to spider analyze data...'
cd /usr/project/hzdata
nohup python analyze.py > log/analyze.log 2>&1 &
