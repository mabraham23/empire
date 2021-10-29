#!/bin/bash
export COUNTRY=2
export PLAYER=2
export EMPIREPORT=2836
export EMPIREHOST=empire
stop=0
./explore.py
while [ $stop != 1 ]; do
  ./data_dump.bash
  ./search.bash
  stop=$?
  ./wait_for_update.bash
done
