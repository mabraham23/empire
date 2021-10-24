#!/bin/bash
export COUNTRY=13
export PLAYER=13
export EMPIREPORT=2833
export EMPIREHOST=empire
stop=0
./explore.py
while [ $stop != 1 ]; do
  ./data_dump.bash
  ./search.bash
  stop=$?
  ./wait_for_update.bash
done