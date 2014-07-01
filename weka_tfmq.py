#!/usr/bin/env python
# -*- coding: utf-8 -*-


# weka_tfmq.ijm
#
# OMERO script
# Weka Fast RF segmentation using TaskFarmerMQ
#
# Joaquin Correa, Data and Analytics services
# JoaquinCorrea@lbl.gov
# National Energy Research Scientific Computing Center
# Lawrence Berkeley National Laboratory
# 2014

"""


"""


OMERO_HOME="/project/projectdirs/ngbi/omero5/OMERO.server"
GSCRATCH = "/global/scratch2/sd/jcorrea"
cache_dir = os.path.join(GSCRATCH, 'ngbi/tmp')
qsub_path= "/usr/syscom/opt/torque/4.2.6/bin/qsub"

import os
import omero
import pickle

from omero.gateway import BlitzGateway
import omero.scripts as scripts
from omero.rtypes import *
import omero.util.script_utils as script_utils
import numpy as np
from numpy import zeros, hstack, vstack
import sys, traceback, subprocess, os

import time
import timeit

import matplotlib as mpl
import scipy as sp
import PIL as pil
import numpy as np

import omero.cli as cli

from omero.rtypes import rtime, rlong, rstring, rlist, rint
from omero_model_ExperimenterI import ExperimenterI
from omero_model_ExperimenterGroupI import ExperimenterGroupI
from omero_model_PermissionsI import PermissionsI

import tempfile
import subprocess

import math

OMERO_PATH=os.path.join(OMERO_HOME,"bin/omero")
SCRIPT_PATH=os.path.join(OMERO_HOME,"lib/scripts/OMERO.HPC")
IMAGEJ_PATH=os.path.join(SCRIPT_PATH, "resources/ImageJ/ImageJ-linux64")
XVFBRUN_PATH=os.path.join(SCRIPT_PATH,"resources/scripts/xvfb-run")
PBS_GEN=os.path.join(SCRIPT_PATH,"resources/scripts/pbsgen_tfmq.sh")
MACRO_PATH = os.path.join(SCRIPT_PATH,"resources/macros/stack_out.ijm")
MACRO_PATH2 = os.path.join(SCRIPT_PATH,"resources/macros/weka_tfmq.ijm")

def weka_segmentation(conn, scriptParams, uuid):


    model = scriptParams["Segmentation_model"]
    model_path=model

    user = conn.getUser()
    user = user.getName()
    # print("user: %s" % (user))

    # print(model_path)

    images, logMessage = script_utils.getObjects(conn, scriptParams)
    if not images:
        return None, None, logMessage
    imageIds = [i.getId() for i in images]

    for iId in imageIds:

        tmpdir_stack = tempfile.mkdtemp(dir=cache_dir)
        tmpdir_out = tempfile.mkdtemp(dir=cache_dir)

        image = conn.getObject("Image", iId)
        dataset = image.getParent().getId()

        sizeZ = image.getSizeZ()
        print(sizeZ)

        # job_liner=[]

        all_jobs = open("%s.job" % (os.path.join(cache_dir, tmpdir_out.split('/')[-1])), 'w+')

        for z in range(sizeZ):
            plane = image.renderImage(z, 0)
            img_path = os.path.join(tmpdir_stack, "plane_%02d.tiff" % z)
            plane.save(img_path)

            ijmacro_args = "%s*%s/*%s" % (img_path, tmpdir_out, model_path)

            img_path2 = os.path.join(tmpdir_out, "plane_%02d.tiff" % z)
            job_liner=("%s -a %s -Xmx2g -- -macro %s %s -batch:%s:0 \n" % (XVFBRUN_PATH, IMAGEJ_PATH, MACRO_PATH2, ijmacro_args, img_path2))
            all_jobs.writelines(job_liner)

        all_jobs.close()

        system = scriptParams["System"]
        wtime = scriptParams["Wall_time"]
        pmem = scriptParams["Private_memory"]

        pbs_file = "%s.pbs" % (os.path.join(cache_dir, tmpdir_out.split('/')[-1]))

        nodes = int(math.ceil(((2.00*sizeZ)+0.15*(2.00*sizeZ))/48))

        stack_args = "%s/" % (tmpdir_out)
        image_name = image.getName()
        qsub_cmd = ". %s %s %s %s %s %s %s %s %s %s %s %s > %s" % (PBS_GEN, user, dataset, image_name, uuid, MACRO_PATH, stack_args, tmpdir_out, wtime, pmem, all_jobs.name, nodes, pbs_file)

        print(qsub_cmd)
        os.system(qsub_cmd)

        enableKeepAlive_time = (72*60*60)
        conn.c.enableKeepAlive(enableKeepAlive_time)
        os.system("ssh %s '%s %s'" % (system, qsub_path, pbs_file))

def runAsScript():

    dataTypes = [rstring('Image')]

    models_path=os.path.join(SCRIPT_PATH, "sample/classifiers/")
    systems=['carver']

    segmentationModel = []
    for file in os.listdir(models_path):
        if file.endswith(".model"):
            segmentationModel.append(str(os.path.join(models_path,file)))

    client = scripts.client('weka_tfmq.py', """Segment a dataset using Random Forest and a known classifier""",

    scripts.String("Data_Type", optional=False, grouping="1",
        description="Pick Images by 'Image' ID or by the ID of their 'Dataset'", values=dataTypes, default="Image"),

    scripts.List("IDs", optional=False, grouping="1.1",
        description="List of Dataset IDs or Image IDs to process.").ofType(rlong(0)),

    scripts.String("Segmentation_model", optional=False, grouping="2",
        description="Select model", values=segmentationModel, default=segmentationModel[0]),

    scripts.String("System", optional=False, grouping="3",
        description="Select the system", values=systems, default=systems[0]),

    scripts.String("Wall_time", grouping="3.1",
        description="Wall time", default='0:30:00'),

    scripts.String("Private_memory", grouping="3.2",
        description="Private memory", default='4GB'),

    scripts.Bool("Big_memory_nodes", grouping="3.2.1",
        description="Big memory nodes", default='False'),

    scripts.String("Nodes", grouping="3.3",
        description="Nodes", default='1'),

    scripts.String("PPN", grouping="3.4",
        description="PPN", default='5'),

    version = "0",
    authors = ["Joaquin Correa", "Data and Analytics services"],
    institutions = ["National Energy Research Scientific Computing Center (NERSC)"],
    contact = "JoaquinCorrea@lbl.gov",
    )

    try:
        session = client.getSession();

        scriptParams = {}
        for key in client.getInputKeys():
            if client.getInput(key):
                scriptParams[key] = client.getInput(key, unwrap=True)

        conn = BlitzGateway(client_obj=client)

        admin = conn.getAdminService()
        uuid = admin.getEventContext().sessionUuid
        weka_segmentation(conn, scriptParams, uuid)

    finally:
        client.closeSession()

if __name__ == "__main__":
    runAsScript()
