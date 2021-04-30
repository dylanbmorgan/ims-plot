#!/bin/bash
# mg09.sh
# Run multiple jobs consecutively using Guassian 09
# Author: Dylan Morgan

arg_inp() {
    arg_files=( "$@" )

    if [[ $# -eq 0 ]]; then
        man_inp
    else
        echo -e "\n$# files selected: ${arg_files[*]}"
        check_files
    fi
}

man_inp() {
    echo -e "\nSpecify files to run:"
    read -re input_files
    arg_files=()
    arg_files+=($input_files)
    echo -e "\n${#arg_files[@]} files selected: ${arg_files[*]}"
    check_files
}

check_files() {
    echo
    read -rp "Are these the correct files? (y/n) " verify

    for file in "${arg_files[@]}"; do 
        if [[ -z "${arg_files[*]}" ]]; then
            echo -e "\nNo files were Specified!\n"
            man_inp
        elif [[ $file != *.com ]]; then
            echo -e "\n One or more of the files have the wrong extension or no extension."
            man_inp
        else
            usr_verification
        fi
    done
}

usr_verification() {
    if [[ "$verify" == "y" ]] || [[ "$verify" == "yes" ]]; then
        run_jobs
    elif [[ "$verify" == "n" ]] || [[ "$verify" == "no" ]]; then
        man_inp
    else
        echo -e "\nNot a valid answer. Repeat your input or press ctrl+c to exit:"
        check_files
    fi
}

run_jobs() {
    for file in "${arg_files[@]}"; do
        rm_f_ext=${file%.com}
        base_input_files+=( "${rm_f_ext}" )
    done

    echo -e "\nRunning ${#arg_files[@]} jobs..."

    for value in "${base_input_files[@]}"; do
        g09 "$value.com" "$value.log" &&
            echo "$value.com > $value.log completed successfully!" ||
            echo "There was an issue with running $value.com > $value.log"
    done &&
        echo -e "\nPopty ping!\n" 
    
    exit 0
}


arg_inp "$@"

