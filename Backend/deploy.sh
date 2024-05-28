#!/usr/bin/env bash

WORKING_DIRECTORY="~/www/seng2021deploy"

USERNAME="h18abrownie"
SSH_HOST="ssh-h18abrownie.alwaysdata.net"

rm -rf ./**/__pycache__ ./**/.pytest_cache > /dev/null
scp -r ./requirements.txt ./src "$USERNAME@$SSH_HOST:$WORKING_DIRECTORY"
ssh "$USERNAME@$SSH_HOST" "cd $WORKING_DIRECTORY && source env/bin/activate && pip3 install -r requirements.txt"
