#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

temp_file=$(mktemp)
python3 $DIR/sshh.src/main.py --connect "$1" >> $temp_file

cat $temp_file
echo ""
bash $temp_file
rm -rf $temp_file