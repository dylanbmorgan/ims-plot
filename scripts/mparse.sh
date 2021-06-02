#!/bin/bash
# mparse.sh
# Parse data from multiple log files at once
# Author: Dylan Morgan

arg_inp() {
    arg_files=( "$@" )

    if [[ $# -eq 0 ]]; then
        man_inp
    else
        for file in "${arg_files[@]}"; do
            if [[ $file = *.com ]]; then
                com_files+=("$file")
            elif [[ $file = *.log ]]; then
                log_files+=("$file")
            else
                echo -e "\nOne or more file(s) have the wrong extension or no extension."
                echo "Specify the file(s) manually or press ctrl+c to exit."
                man_inp
            fi
        done
        check_files
    fi
}

man_inp() {
    echo -e "\nSpecify input (.com) files:"
    read -re input_files
    com_files=()
    com_files+=($input_files)

    echo -e "\nSpecify output (.log) files to parse:"
    read -re output_files
    log_files=()
    log_files+=($output_files)
    check_files
}

check_files() {
    if [[ "${#com_files[@]}" -eq "${#log_files[@]}" ]]; then
        if [[ -z "${com_files[*]}" ]] || [[ -z "${log_files[*]}" ]]; then
            echo -e "\nNo files were Specified. Please re-enter or press ctrl+c to exit."
            man_inp
        else
            echo -e "\n${#com_files[@]} input and ${#log_files[@]} output files selected."
            echo -e "\nInput files: ${com_files[*]}\n"
            echo -e "Output files: ${log_files[*]}\n"
            read -rp "Are these files correct? (y/n) " verify
            usr_verification
        fi
    else
        echo -e "\nInput and output files do not match. Please re-enter or press ctrl+c to exit:"
        man_inp
    fi
}

usr_verification() {
    if [[ "$verify" == "y" ]] || [[ "$verify" == "yes" ]]; then
        parse_files
    elif [[ "$verify" == "n" ]] || [[ "$verify" == "no" ]]; then
        man_inp
    else
        echo -e "\nNot a valid answer. Repeat your input or press ctrl+c to exit:"
        check_files
    fi
}

parse_files() {
    echo -e "\nparsing data from ${#log_files[@]} files..."

    enum_no=( $(seq 1 "${#com_files[@]}") )

    for i in "${!com_files[@]}"; do
        log_parser.py "-fparsed_data_${enum_no[i]}.txt" "${com_files[i]}" "${log_files[i]}" | xargs printf "%s %s %s "
        echo -e "\n"
        # TODO: Automatically mkdir parsed data folder and save everything into there
    done &&
        cowsay "Popty ping!" ||
        cowsay "There was an issue with parsing one or more of the files :("
}


arg_inp "$@"
