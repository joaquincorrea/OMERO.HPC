#!/bin/csh -fx
rm -f ./out-env/*
rm -f *.done
rm -f *.e*
rm -f *.o*
module load python 
#module load taskfarmermq
module load taskfarmermq/2.1

qsub -t worker_mendel.q
tfmq-client -i taskEnv.lst -w 0 -r 1
