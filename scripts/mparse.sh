#!/bin/bash
# mparse.sh
# Parse data from multiple log files at once
# Author: Dylan Morgan

specify_files

specify_files () {
    echo -e "\nSpecify input (.com) files:"
    read -e input_files
    com_files+=($input_files)

    echo -e "\nSpecify output (.log) files to parse:"
    read -e output_files
    log_files+=($output_files)

    if [ "${#com_files[@]}" != "${#log_files[@]}" ]; then
        echo -e "\n Input and output files do not match. Please re-enter:"
        specify_files
    else 
        echo -e "\n${#com_files[@]} input and ${#log_files[@]} ouput files selected"
        check_files
    fi
}

check_files () {
    echo
    read -p "Are these files correct? (y/n) " verify

    if [ -z "${com_files}" ] || [ -z "${log_files}" ]; then 
        echo -e "\nNo files were Specified!"
        specify_files
    else 
        usr_verification
    fi
}

usr_verification () {
    if [ "$verify" == "y" ] || [ "$verify" == "yes" ]; then
        parse_files
    elif [ "$verify" == "n" ] || [ "$verify" == "no" ]; then
        echo; retry
    else
        echo -e "\nNot a valid answer. Repeat your input or press ctrl+c to exit:"
        check_files
    fi
}

parse_files () {
    echo -e "\nparsing data from ${#log_files[@]} files..."
    
    until [ $(seq 1 ${#log_files[@]}) ]; do 

    for 

    for num com log in $com_files $log_files 
        "log_parser.py $com $log -o .parsed_data_$num.txt"
    done &&

    echo -e "\nPopty ping!\n" || 
    echo -e "\nThere was an issue with running 1 or more of the files. Check your input files to make sure there are no errors.
    Otherwise, try reducing the number of ghost atoms per input file.\n"  # Change these lines
}

