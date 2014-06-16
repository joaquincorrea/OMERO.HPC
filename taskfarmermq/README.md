taskfarmerMQ
============

Farming out user tasks to workers on cluster systems

First, you need to describe a list of tasks with specifying output(s) in a file
and submit the workers (as many as you need). Second, when you start the tool
with your task list file, it sends the task to a message queue in the message
broker. The workers pop the messages from the broker and starts working and
checking the return co de and the output file(s) and return the result back to
the message queue. Lastly, taskfarmerMQ collects the results from the queue and
create a report file. 

Syntax

    tfmq-client [-h] -i TASKFILENAME [-q TASKQUEUENAME] [-w] [-r] [-m] [-l DEBUGLEVEL]
                   
    -i,--tf: Set user task list file
    
    -q,--tq: *THIS IS OPTIONAL* Set user-specified queue name (*NOTE: If you set
    your queue name with this option, you SHOULD set the same queue name when
    you start the worker using -q/--tq). If not set, a default queue name will
    be used.
    
    -w,--reuse: Disable worker termination option. If it is not set, all workers
    will be terminated after completion; If set, all workers will stay running
    for being reused to process other tasks. 
    
    -r,--report: Enable printing the resource usages like cpu and memory usage,
    and runtime for all workers running. If you set this, the client will print
    out the resource usage in the following format:
    
    <host_name>,<parent_pid>,<user_command_pid>,<cpu_usage>,<memory_usage(RSS)>,
    <memory_usage(VMS)>,<run_time>,<node_mem_avail(%)>,<num_workers_on_the_node>
    
    
    -m,--nodemem: Enable warninng on the memory usage (%) if memory
    usage on a node is over the specified threshold (default: 90%)

    

    tfmq-worker [-h] [-q TASKQUEUENAME] [-b HBINTERVAL] [-t TIMEOUT] [-l DEBUGLEVEL] [-z]

    -q/--tq: Set user-defined queue name. If you set a different queue name for
    running tfmq-client, you SHOULD set the same name when you run the worker.
    
    -b/--heartbeat: Set the time interval to send heartbeat
    to the client. Default: 10 seconds.

    -t/--timeout: Set the timer for worker to terminate. If there is no request
    from the client for the specified seconds, the worker terminates itself.
    Default: 30 seconds
    
    -z/--zerofile: Allow zero-sized output file(s)


Task list file format

    After the user command is completed, each worker checks if the specified
    output files exist and if those files are not zero-sized. Multiple output
    files can be listed using the comma as a delimiter.

    ex)
    uname -a > ./out-uname/2.uname.out:./out-uname/2.uname.out:0
    uname -a > ./out-uname/3.uname.out:./out-uname/2.uname.out,./out-uname/3.uname.out:0
    uname -a > ./out-uname/4.uname.out::0
    
    ex2)
    /jgi/tools/bin/blastall -b 100 -v 100 -K 100 -p blastn -S 3 -d ./data/hs.m51.D4.diplotigs+fullDepthIsotigs.fa -e 1e-10 -F F -W 41 -i 
    ./data/blast_query_1_160.fna -m 8 -o ./out-blastn/test1.m8.bout:./out-blastn/test1.m8.bout:0
    /jgi/tools/bin/blastall -b 100 -v 100 -K 100 -p blastn -S 3 -d ./data/hs.m51.D4.diplotigs+fullDepthIsotigs.fa -e 1e-10 -F F -W 41 -i 
    ./data/blast_query_1_160.fna -m 8 -o ./out-blastn/test2.m8.bout:./out-blastn/test1.m8.bout,./out-blastn/test2.m8.bout:0
    /jgi/tools/bin/blastall -b 100 -v 100 -K 100 -p blastn -S 3 -d ./data/hs.m51.D4.diplotigs+fullDepthIsotigs.fa -e 1e-10 -F F -W 41 -i 
    ./data/blast_query_1_160.fna -m 8 -o ./out-blastn/test3.m8.bout:./out-blastn/test4.m8.bout:0


How to test

1. Module load

   $ module load taskfarmermq/2.1

2. Start the worker 

   $ tfmq-worker -b 5 -t 30 -q test

3. Start the client on the other terminal

   $ tfmq-client -i task1.lst -r -q test


How to run on cluster

1. qsub -t 1-2 worker_mendel.q
2. Start the client with user task list

(Also you can start the client in your batch script)


Related Documents

https://docs.google.com/a/lbl.gov/presentation/d/1OU1-Tu8XGSOCcM6xQ7P0zn_evM8FynJQ69Qi7iuJMhM/edit

https://docs.google.com/a/lbl.gov/document/d/1cW3ttWAXrVTRTe71cU4T0adBFwhi-I25F6Enhi1HYX0/edit


Acknowledgement

- Shane Canon 
- Kirsten Fagnan
- Ernest Szeto (beta testing) 
