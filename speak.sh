#!/bin/bash

echo $1 | \
  piper --model en_GB-southern_english_female-low --output-raw | \
  aplay -r 16400 -f S16_LE -t raw -

