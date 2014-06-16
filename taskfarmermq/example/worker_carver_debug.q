#!/bin/bash -l
#PBS -N carver_tfmq_test
#PBS -q debug
#PBS -l nodes=1:ppn=8
#PBS -l pvmem=2GB
#PBS -l walltime=00:30:00
#PBS -V

module load python
cd $PBS_O_WORKDIR
sh ./run_8_tfmq-workers.sh

##
## To start the client, 
## tfmq-client -i taskEnv.lst -w 0 -r 1 -q tfmqtaskqueue
##
