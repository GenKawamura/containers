#!/usr/bin/python

import os, sys, getopt, time, commands
import re

def Usage ():
    command_name = "tensorflow_cluster_instance.py"

    print "Usage: " + command_name + " [-p][-w][-n] num_of_workers [-i] start_ip [-t] task_id [-h][-v]"
    print "-p, --parameter_server"
    print "-w, --worker"
    print "-n, --num_of_workers"
    print "-i, --start_ip"
    print "-t, --task_id"
    print "-h, --help"
    print "-v, --version"
    print ""
    print "Report bugs to <gen.kawamura@cern.ch>."

def Version ():
    print "version 0.1.0"

def main():

    """    command line read    """
    job_name = ""
    num_of_workers = 2
    base_ip = "255.255.255"
    start_ip = ""
    task_index = ""

    try:
        options, remainder = getopt.getopt(sys.argv[1:], 'hvpwn:i:t:', ['help', 'version', 'parameter_server', 'worker', 'num_of_workers=', 'start_ip=', 'task_index='])
    except getopt.GetoptError:
        Usage()
        print "called exception"
        sys.exit(1)

    for opt, arg in options:
        if opt in ('-v', '--version'):
            Version()
            sys.exit(0)
        elif opt in ('-h', '--help'):
            Usage()
            sys.exit(0)
        elif opt in ('-p', '--parameter_server'):
            job_name = "ps"
        elif opt in ('-w', '--worker'):
            job_name = "worker"
        elif opt in ('-n', '--num_of_workers'):
            num_of_workers = int(arg)
        elif opt in ('-i', '--start_ip'):
            start_ip = str(arg)
        elif opt in ('-t', '--task_index'):
            task_index = int(arg)


    """ check parameters """
    print "job_name       = " + job_name 
    print "num_of_workers = " + str(num_of_workers)
    print "start_ip       = " + start_ip
    print "task_index     = " + str(task_index)

    if num_of_workers == "" or start_ip == "" or job_name == "" or task_index == "":
        Usage()
        sys.exit(1)

    """ Generating TF cluster """
    ## Init
    tf_cluster = {}
    tf_parameter_servers = []
    tf_workers = []

    ## Making parameter server
    tf_parameter_servers.append(start_ip + ":2222")
    tf_cluster["ps"] = tf_parameter_servers

    ## Making workers
    base_ip = re.split("\.", start_ip)
    for x in range(1, num_of_workers+1):
        worker_ip = str(base_ip[0]) + "." + str(base_ip[1]) + "." + str(base_ip[2]) + "." + str(int(base_ip[3]) + x)
        tf_workers.append(worker_ip + ":2222")
    tf_cluster["worker"] = tf_workers

    print "tf_cluster = " + str(tf_cluster)


    """ Opening a listner """
    ## To make listners in tensorflow cluster, the following codes will 
    ## be executed by parameter server and worker nodes.
    import tensorflow as tf

    ## Opening a cluster listner
    cluster = tf.train.ClusterSpec(tf_cluster)
    server = tf.train.Server(cluster, job_name=job_name, task_index=task_index)

    ## Wait
    ##raw_input("Listening in tf.train.server")



if __name__ == '__main__':
    main()

