#!/usr/bin/env bash
echo 'begin to spider analyze data...'
cd /usr/project/hzdata
nohup python hzdata/analysis.py >> log/analysis.log 2>&1 &
