#!/bin/bash

# provide file to load in from and to save to using command line
resolved_uris="$1"
unique_resolved_uris="$2"

> "$unique_resolved_uris"

# sort and filter all unique URIs
sort -u "$resolved_uris" > "$unique_resolved_uris"

echo "unique links have been saved to $unique_resolved_uris"
