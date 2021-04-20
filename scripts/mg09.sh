#!/bin/bash
# mg09.sh
# Run multiple jobs consecutively using Guassian 09
# Author: Dylan Morgan

check_files () {
    echo
    read -p "Are these files correct? (y/n) " verify

    if [ -z "${arg_files}" ]; then 
        echo -e "\nNo files were Specified!\n"
        retry
    else 
        usr_verification
    fi
}

retry () {
    echo -e "Enter the files to be run or press ctrl+c to exit:"
    read -e input_files
    arg_files+=($input_files)
    echo -e "\n${#arg_files[@]} files selected: ${arg_files[@]}"
    check_files
}

usr_verification () {
    if [ "$verify" == "y" ] || [ "$verify" == "yes" ]; then
        run_jobs
    elif [ "$verify" == "n" ] || [ "$verify" == "no" ]; then
        echo; retry
    else
        echo -e "\nNot a valid answer. Repeat your input or press ctrl+c to exit:"
        check_files
    fi
}

run_jobs () {
    for file in ${arg_files[@]}; do
        rm_fext=${file%.com}
        base_input_files+=( "${rm_fext}" )
    done

    echo -e "\nRunning ${#arg_files[@]} jobs..."

    for value in "${base_input_files[@]}"; do
        g09 $value'.com' $value'.log' &&
        echo "$value.com > $value.log completed successfully!" ||
        echo "There was an issue with running $value.com > $value.log"
    done &&

    echo -e "\nPopty ping!\n"
}

arg_files=( "$@" )

if [ $# != 0 ]; then
    echo -e "\n$# files selected: ${arg_files[@]}"
    check_files
else
    echo -e "\nSpecify files to run:"
    read -e input_files
    arg_files+=($input_files)
    echo -e "\n${#arg_files[@]} files selected: ${arg_files[@]}"
    check_files
fi

