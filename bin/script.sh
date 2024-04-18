#!/bin/bash

ruff check --output-format json | jq '(group_by(.code) | map({code: (.[0].code + " - " + .[0].message), messages: [.[] | (.filename + ":" + (.location.row | tostring) + ":" + (.location.column | tostring)) ]})) | sort_by(.messages | length)' > /tmp/file2132415649845321.txt

echo "Nomber of issues" $(jq "map(.messages | length) | add " /tmp/file2132415649845321.txt)

cat /tmp/file2132415649845321.txt
