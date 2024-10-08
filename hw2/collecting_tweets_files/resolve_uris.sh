#!/bin/bash

# provide file to load in from and to save to via the command line argument
load_file="$1"
save_file="$2"

# delete any previously saved copy of save file
> "$save_file"

# for each URI:
while IFS= read -r uri; do
    
    final_uri="$uri"

    # keeps iterating through the URIs until you reach the final resolvced one
    while true; do
        # fetch the headers using curl
        response=$(curl -IL --silent --max-time 10 --location "$final_uri" 2>/dev/null)
        if [ $? -ne 0 ]; then
            echo "Request to $final_uri timed out or failed"
            break
        fi

        # get the last HTTP status and then check if it's 200
        http_status=$(echo "$response" | grep HTTP | tail -n 1 | awk '{print $2}')

        # if the status is 200, check what the resolved URL is and then save into the file
        if [ "$http_status" == "200" ]; then
            final_uri=$(echo "$response" | grep -i "^Location:" | tail -n 1 | cut -d ' ' -f2-)
            if [[ "$final_uri" =~ ^http ]]; then
                echo "$final_uri" >> "$save_file"
            fi
            break
        fi

        # check for a new resolved URI
        resolved_uri=$(echo "$response" | grep -i "^Location:" | tail -n 1 | cut -d ' ' -f2-)

        # if there’s no further resolved URI, we have found the final location and can end the loop
        if [ -z "$resolved_uri" ]; then
            echo "No further redirection for $final_uri"
            break
        fi

        # updates the final_uri, but it might not actually be 'final': the loop continues
        final_uri="$resolved_uri"
    done
    
done < "$load_file"

echo "final URIs are now saved to $save_file"
