#!/bin/bash
module load blast
blast_exec=`which blastn`
$blast_exec  -num_threads 2 -db ./data/hs.m51.D4.diplotigs+fullDepthIsotigs.fa -evalue 1 -query ./data/9999.unassembled_illumina.faa -out ./out-blastn/test1.m8.bout

