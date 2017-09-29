#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


function print_avail () {
    python3 $DIR/sshh.src/main.py
}



function connect_to_server () {
    temp_file=$(mktemp)
    python3 $DIR/sshh.src/main.py --connect "$1" >> $temp_file

    cat $temp_file
    echo ""
    bash $temp_file
    rm -rf $temp_file
}


if [[ $# -eq 0 ]]; then
    print_avail
    exit 0
fi

while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -l|--list)
            print_avail
            exit 0
        ;;
        *)
            SERVER="$2"
            shift
            shift
            connect_to_server "$SERVER"

        ;;
    esac
done
