#!/bin/bash

echo Stopping server
test -e ~/run.pid && kill $(cat ~/run.pid)
sleep 30
echo Pulling from GitHub
git pull
echo Starting server again
sleep 30
nohup python __init__.py &> ~/log.log &
