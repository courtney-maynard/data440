#!/bin/bash

file_of_links="timemap_test_file.txt"
num_links=1

# want to save the number of mementos during this process, 
# so each file does not need to be revisted in a seperate script

memento_count_output="memento_counts.txt"
: > "$memento_count_output"

while IFS= read -r link; do
    # the json timemap information will be saved to specific numbered json file
    uniq_timemap_file="timemap_files_hw2/link_${num_links}.json"

    # use memgator to gather output and route to a json file
    ./memgator-darwin-amd64 -F 2 -f JSON "$link" > "$uniq_timemap_file"

    # save off the number of mementos found, then zip and save the json file
    memento_count=$(jq '.mementos.list | length' "$uniq_timemap_file")
    gzip "$uniq_timemap_file" 

    # append count to memento count file
    # outputs zero if no mementos were found 
    echo "${memento_count:-0}" >> "$memento_count_output"

    ((num_links++))
done < "$file_of_links"
