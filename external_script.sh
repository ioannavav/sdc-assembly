#!/bin/bash

TESTING_INPUTS=()
DEFAULT_INPUTS=()

while (( "$#" )); do
  case "$1" in
    --testing_inputs)
      shift
      while [[ "$1" != --* && "$#" -gt 0 ]]; do
        TESTING_INPUTS+=("$1")
        shift
      done
      ;;
    --default_inputs)
      shift
      while [[ "$1" != --* && "$#" -gt 0 ]]; do
        DEFAULT_INPUTS+=("$1")
        shift
      done
      ;;
    *)
      echo "Error: Invalid argument"
      exit 1
  esac
done

input_file=${TESTING_INPUTS[0]}
base_name=$(basename $input_file .c)

/bin/bash ./full_works_script.sh "${TESTING_INPUTS[@]}" -- "${DEFAULT_INPUTS[@]}" > intermediate_1.txt

python3 new_parser.py intermediate_1.txt > intermediate_2.txt
python3 dictionary.py intermediate_2.txt > intermediate_3.txt

# Find the limits of the blocks of interest. From now on, we only procede if Final_result.txt is not empty (we have found some interesting differences)
if [ -s intermediate_3.txt ]; then
    python3 new_extract_block_limits.py intermediate_3.txt > intermediate_4.txt
    
    python3 unique_blocks.py intermediate_4.txt > intermediate_4_unique.txt

    while read -r first_string second_string others
    do
      output_file="block_$(date +"%FT%T")---$first_string--$second_string.txt"
      if [[ ${#DEFAULT_INPUTS[@]} -ne 0 ]]; then
          echo "$first_string $second_string ${DEFAULT_INPUTS[@]}" | gdb -batch -x gdb_script.py > $output_file
      else
          echo "$first_string $second_string" | gdb -batch -x gdb_script.py > $output_file
      fi
      clean_output_file="clean_$output_file"
      python3 last_step_parser.py $output_file > $clean_output_file
    done < intermediate_4_unique.txt

    while read -r first_string second_string others
    do
      matched_file=$(ls clean_block_*---${first_string}--${second_string}.txt 2>/dev/null | head -n 1)
      if [ -z "$matched_file" ]; then
        echo "No file matches the pattern: *---${first_string}--${second_string}.txt"
      else
        python3 helper_focus_lined.py $matched_file $others
      fi
    done < intermediate_4.txt

else
    echo "No interesting differences in registers found."
fi


# put intermediate results in a different folder so that we don't get confused
mkdir -p intermediate_results_of_$base_name
mv core_*.txt intermediate_results_of_$base_name 2>/dev/null || true
mv intermediate_*.txt intermediate_results_of_$base_name 2>/dev/null || true
mkdir -p blocks_of_$base_name
mv block_*.txt blocks_of_$base_name 2>/dev/null || true
mkdir -p clean_blocks_of_$base_name
mv clean_block_*.txt clean_blocks_of_$base_name 2>/dev/null || true