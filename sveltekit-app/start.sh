#!/bin/bash
# Script to start on AWS EC2 where node is installed in user directory
# used by systemd
. ~/.nvm/nvm.sh
# note start instead of run as run watches for changes of files and exists directly in systemd
npm run dev
