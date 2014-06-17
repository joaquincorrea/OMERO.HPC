

OMERO.HPC
=========

This is a HPC implementation of [Weka environment] Fast Random Forest that uses a pre-OMERO.fs OMERO server as the front-end.

Requirements
------------

  - [OMERO] server
  - [TaskFarmerMQ]
  - [RabbitMQ]
  - [ImageJ]
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


```sh

```

Configuration
-------------


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
[TaskFarmerMQ]:https://github.com/jjcorreao/OMERO.HPC/tree/master/taskfarmermq
[xvfv]:http://www.x.org/archive/X11R7.7/doc/man/man1/Xvfb.1.xhtml
[Shreyas Cholia]:
[David Skinner]: