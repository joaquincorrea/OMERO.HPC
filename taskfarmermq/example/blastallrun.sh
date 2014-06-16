#!/bin/bash

module load blast
blast_exec=`which blastall`
$blast_exec -b 100 -v 100 -K 100 -p blastn -S 3 -d ./data/hs.m51.D4.diplotigs+fullDepthIsotigs.fa -e 1e-10 -F F -W 41 -i ./data/blast_query_1_160.fna -m 8 -o ./out-blastn/test1.m8.bout

