

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


[Seung-Jin Sul]:https://bitbucket.org/sulsj
[OMERO]:https://www.openmicroscopy.org/
[RabbitMQ]:http://www.rabbitmq.com/
[ImageJ]:http://fiji.sc
[Weka environment]:http://www.cs.waikato.ac.nz/ml/weka/
[xvfb]:
[TaskFarmerMQ]: