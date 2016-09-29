#!/usr/bin/python

import os, sys, getopt, time, commands

def Usage ():
    command_name = "tensorflow_cluster_instance.py"

    print "Usage: " + command_name + " [-p][-w][-n] num_of_workers [-i] IP [-h][-v]"
    print "-p, --parameter_server"
    print "-w, --worker"
    print "-n, --num_of_workers"
    print "-i, --start_ip"
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
    start_ip = ""

    try:
        options, remainder = getopt.getopt(sys.argv[1:], 'hvpwn:i:', ['help', 'version', 'parameter_server', 'worker', 'num_of_workers=', 'start_ip='])
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


    """ check parameters """
    if num_of_workers == "" or start_ip == "" or job_name == "":
        Usage()
        sys.exit(1)

    """ Generating IPs """
    print "job_name       = " + job_name 
    print "num_of_workers = " + str(num_of_workers)
    print "start_ip       = " + start_ip
    sys.exit(0)

    """ Opening a listner """
    ## To make listners in tensorflow cluster, the following codes will 
    ## be executed by parameter server and worker nodes.
    import tensorflow as tf

    ## Opening a cluster listner
    cluster = tf.train.ClusterSpec({
            "ps": [
                "IP_OF_PARAMETER_HOST:2222"
                ],
            "worker": [
                "IP_OF_WORKER_HOST1:2222",
                "IP_OF_WORKER_HOST2:2222"
                ]})

    server = tf.train.Server(cluster, job_name=job_name, task_index=0)


if __name__ == '__main__':
    main()

