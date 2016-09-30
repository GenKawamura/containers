#!/bin/bash

## Single mode
steps="100 200 500 1000 2000 5000 10000"
for step in $steps
do
    [ -e /tmp/single_tf_${step}.log ] && continue
    ./multi-tensorflow -n $step -o -c 0 -s &> /tmp/single_tf_${step}.log
done

## Multi CPU workers
workers="3 5 7 9"
for step in $steps
do
    for worker in $workers
    do
	[ -e /tmp/multi_tf_${worker}__${step}.log ] && continue
	./multi-tensorflow -n $step -w $worker -o -m &> /tmp/multi_tf_${worker}__${step}.log
    done
done
