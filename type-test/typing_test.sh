#!/bin/bash

# Function to display text in light gray
display_text() {
    echo -e "\033[90m$1\033[0m"
}

# Calculate WPM
calculate_raw_wpm() {
    local start_time=$1
    local end_time=$2
    local num_chars=$3
    local elapsed=$((end_time - start_time))

    if [ "$elapsed" -eq 0 ]; then
        echo "Elapsed time is zero, typing speed calculation not possible."
        return
    fi

    local words_typed=$((num_chars / 5)) # Average word length is set as 5 char
    local wpm=$((words_typed * 60 / elapsed))
    echo $wpm
}

sample_random_words() {
    local file_path=$1
    tr ' ' '\n' < $file_path | shuf | head -n 15 | tr '\n' ' '
}


typing_test() {
    local mode=$1  # Add an argument for selecting the mode

    local target_text
    if [[ "$mode" == "random-words" ]]; then
        # If mode is random-words, sample 15 random words from the specified file
        target_text=$(sample_random_words /home/umar.dabhoiwala/scripts/type-test/words.txt)
    else
        # Default behavior: get a random line from strings.txt
        mapfile -t lines < /home/umar.dabhoiwala/scripts/type-test/strings.txt
        target_text=${lines[$RANDOM % ${#lines[@]}]}
    fi

    local input_text
    local start_time
    local end_time

    # Display instructions
    display_text "$target_text"
    echo "Type the above text and press Enter. Press Enter to start."
    read -p "" -s

    start_time=$(date +%s)

    # Capture user input
    echo "Now type:"
    read input_text

    end_time=$(date +%s)

    local num_chars=${#target_text}
    local raw_wpm=$(calculate_raw_wpm $start_time $end_time $num_chars)
    echo "Congratulations! Your raw typing speed is $raw_wpm words per minute."

    # Call perl script to calculate similarity and true wpm
    local results=$(perl /home/umar.dabhoiwala/scripts/type-test/distance.pl "$target_text" "$input_text" $raw_wpm $num_chars)

    echo "$results"

    local similarity=$(echo "$results" | grep 'Similarity' | awk '{print $NF}')
    local true_wpm=$(echo "$results" | grep 'True WPM' | awk '{print $NF}')
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "$timestamp, $true_wpm", "$similarity" >> /home/umar.dabhoiwala/scripts/type-test/typing_test_log.txt

}


typing_test $1