#!/bin/bash
# mg09.sh
# Run multiple jobs using Guassian 09
# Author: Dylan Morgan

check_files () {
    echo
    echo 'Specified files: '${input_files[@]}
    read -p 'Are these files correct? (y/n) ' verify

    if [ ${#input_files[@]} -eq 0 ]; then
        echo
        echo 'No files were Specified!'
        retry
    else
        usr_verification
    fi
}

usr_verification () {
    if [ $verify == y ] || [ $verify == yes ]; then
        run_jobs
    elif [ $verify == n ] || [ $verify == no ]; then
        input_files=()
        echo
        retry
    else
        echo
        echo 'Not a valid answer. Repeat your input or press ctrl+c to exit:'
        check_files
    fi
}

retry () {
    echo 'Enter the files to be run or press ctrl+c to exit:'
    read cliargs
    input_files+=($cliargs)
    check_files
}

run_jobs () {
    for file in ${input_files[@]}; do
        rm_fext=${file%.com}
        base_input_files+=(${rm_fext})
    done

    echo
    echo 'Running jobs...'

    for value in ${base_input_files[@]}; do
        g09 $value.com $value.log
    done &&
    echo 'Popty ping!'; echo ' '
}


input_files=()
echo
read -p 'Specify files to run: ' argfiles
input_files+=($argfiles)
check_files
