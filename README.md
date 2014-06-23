

OMERO.HPC
=========

This is a HPC implementation of [Weka environment] Fast Random Forest that uses a pre-OMERO.fs OMERO server as the front-end.

Requirements
------------

  - [OMERO] server
  - [RabbitMQ]
  - [xvfv]
  
Sample
------
  - images: A set of image files that will work with the given classifier
  - classifier: Weka model file with 5 classes

Python packages
---------------
  - Pika 

How it works
------------
![alt tag](https://raw.github.com/jjcorreao/OMERO.HPC/master/readme/architecture.png)
OMERO/SCRIPT/JOB/TaskFarmerMQ/TFMQ_Client/ImageJ_JOBS


Installation
------------
  - Stop OMERO.server and OMERO.web

```sh
$OMERO_HOME/bin/omero admin stop
$OMERO_HOME/bin/omero web stop
```

  - Clone repository
  
```sh
cd $OMERO_HOME/lib/scripts
mkdir tfmq_segmentation
cd tfmq_segmentation
git clone https://github.com/jjcorreao/OMERO.HPC.git
```

  - Start OMERO.server and OMERO.web

```sh  
$OMERO_HOME/bin/omero admin start
$OMERO_HOME/bin/omero web start
```

Configuration
-------------

  - Edit ```resources/taskfarmermq/Config.py``` to include your RabbitMQ configuration:

```py
RMQ_HOST = ''
RMQ_USER = ''
RMQ_PASS = ''
RMQ_VHOST = ''
RMQ_PORT = ''
```

  - Edit ```weka_tfmq.py``` to include ```GSCRATCH```,  ```cache_dir``` and path to ```qsub```
  
```py
# i.g.
# GSCRATCH = "/global/scratch2/sd/jcorrea"
# cache_dir = "/global/scratch2/sd/jcorrea/ngbi/tmp"
# qsub_path="/usr/syscom/opt/torque/4.2.6/bin/qsub"
GSCRATCH = ""
cache_dir = ""
qsub_path=""
```

Acknowledgements
----------------
  - This work was supported by the Laboratory Directed Research and Development Program of Lawrence Berkeley National Laboratory under U.S. Department of Energy Contract No. DE-AC02-05CH11231
  - [Shreyas Cholia]
  - [David Skinner]
  - [Seung-Jin Sul]


[Seung-Jin Sul]:https://bitbucket.org/sulsj
[OMERO]:https://www.openmicroscopy.org/
[RabbitMQ]:http://www.rabbitmq.com/
[ImageJ]:http://fiji.sc
[Weka environment]:http://www.cs.waikato.ac.nz/ml/weka/
[TaskFarmerMQ]:https://github.com/jjcorreao/OMERO.HPC/tree/master/resources/taskfarmermq
[xvfv]:http://www.x.org/archive/X11R7.7/doc/man/man1/Xvfb.1.xhtml
[Shreyas Cholia]:https://github.com/shreddd
[David Skinner]:https://github.com/deskinner