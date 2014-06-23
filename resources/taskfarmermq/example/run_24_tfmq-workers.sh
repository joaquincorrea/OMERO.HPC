#!/bin/bash -l

module load python
#module load taskfarmermq/2.1

export PATH=$PATH:$(pwd)

for i in {1..24}
do
	tfmq-worker -b 5 -t 20 -q tfmqtaskqueue &
done
wait

 