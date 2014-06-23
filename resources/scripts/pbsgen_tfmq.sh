#!/bin/sh

# ************************************
# jobgen.sh
# 
# PBS file generator for submitting serial jobs to the queue
# 
# Joaquin Correa
# DAS 2014
# NERSC - LBNL
# 
# $ ./pbsgen_tfmq.sh <user> <dataset> <name> <uuid> <ijmacro> <ijmacro args> <outpath> <wtime> <pmem> <all_jobs> <nodes> > job.pbs
# $ qsub job.pbs
# $ rm job.pbs
# ************************************

#ijpath=/global/project/projectdirs/ngbi/resources/ImageJ/ImageJ-linux64
ijpath=$OMERO_HOME/lib/scripts/tfmq_segmentation/resources/ImageJ/ImageJ-linux64
xvfb_path=$OMERO_HOME/lib/scripts/tfmq_segmentation/resources/scripts/xvfb-run
OMERO_BIN=$OMERO_HOME/bin/omero

#$OMERO_HOME/bin/omero admin stop
#$OMERO_HOME/bin/omero web stop
#cd $OMERO_HOME/lib/scripts
#mkdir tfmq_segmentation
#cd tfmq_segmentation
#git clone https://github.com/jjcorreao/OMERO.HPC.git
#$OMERO_HOME/bin/omero admin start
#$OMERO_HOME/bin/omero web start

user=$1
dataset=$2
name=$3
uuid=$4
ijmacro=$5
ijargs=$6
# PBS_O_WORKDIR=$4

ijmacro_name=$(basename "$ijmacro")
ijmacro_name="${ijmacro_name%.*}_${user}_ngbi"

PBS_JOBID=\$PBS_JOBID
PBS_O_WORKDIR=\$PBS_O_WORKDIR
outpath=$7

wtime=$8
pmem=$9

all_jobs=${10}

nodes_v=${11}
ppn_v=8

cat << EOF

#PBS -S /bin/bash
#PBS -q regular
#PBS -N ${ijmacro_name}
#PBS -l walltime=${wtime}
#PBS -e ${PBS_JOBID}.err
#PBS -A ngbi
#PBS -o ${PBS_JOBID}.out
#PBS -l nodes=${nodes_v}:ppn=${ppn_v}:bigmem

module load oracle-jdk/1.7_64bit

export _JAVA_OPTIONS='-Djava.io.tmpdir=$SCRATCH -XX:-UseParallelGC'

cd ${PBS_O_WORKDIR}

module load python_base

source ${VENV}/bin/activate

# taskfarmeMQ listener
${TFMQ_PATH}/run_8_tfmq-workers.sh &

# taskfarmeMQ client
${TFMQ_PATH}/tfmq-client -i ${all_jobs}

# Stack merge
${xvfb_path} -a ${ijpath} -- -macro ${ijmacro} ${ijargs} -batch

ssh jcorrea@sgn02 'source ~/.bashrc; . /usr/share/Modules/init/bash; source ${OMERO_ENV}; omero import -s sgn02 -d ${dataset} -n ${name} ${outpath}/segmented_map.tif -k ${uuid}'

EOF
