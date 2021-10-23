#!/bin/bash
python3 search.py > commands.txt
egrep '^(move|distribute|capital|threshold|designate|build)' commands.txt > only_commands.txt
empire < only_commands.txt
if [ -s only_commands.txt ]; then
  exit 0
else
  exit 1
fi
