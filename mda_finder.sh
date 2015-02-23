#!/bin/bash

find $1 -type f -exec sh -c "echo ---------------- ; echo {};tail -n +2 {} | grep --color=auto -oP \"[0-9a-zA-Z|_]+\([^\)]*\)(\.[^\)]*\)+)?\" " \;
