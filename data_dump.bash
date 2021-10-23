#!/bin/bash
empire << EOF
xdump sect * | ./data/xdump_parser.py
xdump country * | ./data/xdump_country.py
xdump ship * | ./data/xdump_ship.py
EOF
