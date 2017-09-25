#!/bin/bash


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

_sshh () {
    local cur=${COMP_WORDS[COMP_CWORD]}
    local hints=$(python3 /usr/bin/sshh.src/main.py --list)
    COMPREPLY=( $(compgen -W "$hints" -- $cur) )
}
complete -F _sshh sshh
