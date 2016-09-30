#!/bin/bash

## Variables to measure performance
steps="100 200 500 1000 2000 5000 10000"
workers="3 5 7"
result_file1="/tmp/tensorflow-peformance-time.csv"
result_file2="/tmp/tensorflow-peformance-event.csv"


usage="$0 {single|multi|result}"
[ $# -eq 0 ] && echo "$usage" && exit 0


get_processing_time(){
    local file=$1
    local processing_time=$(grep "Processing Time" $file | sed -e "s/Processing Time = //g")
    [ -z "$processing_time" ] && return 1
    echo "$processing_time"
}

average_events_per_sec(){
    local file=$1

    local events=$(grep "examples\/sec" $file | perl -pe  "s/^.*\((.*?) examples.*/\1/g")
    local N=$(echo "$events" | wc -l)
    local sum_events=$(echo $events | perl -pe  "s/ / + /g")
    [ -z "$events" ] && return 1
    echo "( $sum_events ) / $N" | bc -l
}


case $1 in
    single)
        ## Running Single mode
	for step in $steps
	do
	    [ -e /tmp/single_tf_${step}.log ] && continue
	    ./multi-tensorflow -n $step -o -c 0 -s &> /tmp/single_tf_${step}.log
	done
	;;
    multi)
        ## Running Multi CPU workers
	for step in $steps
	do
	    for worker in $workers
	    do
		[ -e /tmp/multi_tf_${worker}__${step}.log ] && continue
		./multi-tensorflow -n $step -w $worker -o -m &> /tmp/multi_tf_${worker}__${step}.log
	    done
	done
	;;
    result)
	## Writing header
	echo "jobs;steps;processing_time"  > $result_file1
	echo "jobs;steps;events_per_sec"  > $result_file2

	echo "Outputting results of single mode [$result_file1, $result_file2]"
	for step in $steps
	do
	    ## Results of single mode
	    if [ -e /tmp/single_tf_${step}.log ]; then

		processing_time=$(get_processing_time /tmp/single_tf_${step}.log)
		events_per_sec=$(average_events_per_sec /tmp/single_tf_${step}.log)

		worker=1
		[ -z "$processing_time" ] && echo "No processing time info [/tmp/single_tf_${step}.log]"
		[ ! -z "$processing_time" ] && echo "$worker;$step;$processing_time" >> $result_file1
		[ ! -z "$events_per_sec" ] && echo "$worker;$step;$events_per_sec" >> $result_file2
	    fi
	done

	echo "Outputting results of multi-cpu mode [$result_file1, $result_file2]"
	for step in $steps
	do
	    ## Results of multi-CPU mode
	    for worker in $workers
	    do
		if [ -e /tmp/multi_tf_${worker}__${step}.log ]; then
		    processing_time=$(get_processing_time /tmp/multi_tf_${worker}__${step}.log)
		    events_per_sec=$(average_events_per_sec /tmp/multi_tf_${worker}__${step}.log)

		    [ -z "$processing_time" ] && echo "No processing time info [/tmp/multi_tf_${worker}__${step}.log]"		    
		    [ ! -z "$processing_time" ] && echo "$worker;$step;$processing_time" >> $result_file1
		    [ ! -z "$events_per_sec" ] && echo "$worker;$step;$events_per_sec" >> $result_file2
		fi
	    done
	done
	;;
    *)
	echo "$usage"
	;;
esac


