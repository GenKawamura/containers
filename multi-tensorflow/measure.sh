#!/bin/bash

## Single mode
for step in "100 200 500 1000 2000 5000 10000 20000"
do
    ./multi-tensorflow -n $step -o
    ./multi-tensorflow -c 0 -s &> /tmp/single_tf_${step}.log
done
