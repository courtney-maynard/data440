#!/bin/bash

uris_file="1000_uris_hw3.txt"
hashmap_file="hashmaps_hw3.txt"

# delete existing hashmaps file
> "$hashmap_file"

# read in each URI from the 1000
while IFS= read -r each_uri; do
    
    # create the hash
    hash_val=$(echo -n "$each_uri" | md5 | awk '{print $1}')
    
    # download html and save in a file with the hash value as its name
    curl "$each_uri" > "raw_html_files/${hash_val}.html"
    
    # save add to hash mapping file
    echo "$hash_val $each_uri" >> "$hashmap_file"
    
done < "$uris_file"
